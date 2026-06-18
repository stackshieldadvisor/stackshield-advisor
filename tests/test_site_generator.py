import re
import shutil
import tempfile
import unittest
from pathlib import Path


class StaticSiteGenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_build_outputs_multilingual_homepages_with_hreflang(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        for lang in ["en", "fr", "es", "de"]:
            page = self.tmpdir / lang / "index.html"
            self.assertTrue(page.exists(), f"Missing homepage for {lang}")
            html = page.read_text(encoding="utf-8")
            self.assertIn('rel="alternate" hreflang="en"', html)
            self.assertIn('rel="alternate" hreflang="fr"', html)
            self.assertIn('rel="alternate" hreflang="es"', html)
            self.assertIn('rel="alternate" hreflang="de"', html)
            self.assertIn('rel="alternate" hreflang="x-default"', html)

    def test_affiliate_disclosure_is_visible_on_commercial_pages(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        commercial_page = self.tmpdir / "en" / "best-backup-software-small-business" / "index.html"
        self.assertTrue(commercial_page.exists())
        html = commercial_page.read_text(encoding="utf-8")
        self.assertIn("Affiliate disclosure", html)
        self.assertIn("we may earn a commission", html)
        self.assertIn("Sponsored placements are clearly marked", html)

    def test_recommender_contains_conversion_cta_without_collecting_personal_data(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        recommender = self.tmpdir / "en" / "small-business-cyber-stack-recommender" / "index.html"
        self.assertTrue(recommender.exists())
        html = recommender.read_text(encoding="utf-8")
        self.assertIn("Get my recommendation", html)
        self.assertIn("No email required", html)
        self.assertNotRegex(html, re.compile(r'<input[^>]+type=["\']email["\']', re.I))

    def test_sitemap_contains_core_multilingual_urls(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        sitemap = (self.tmpdir / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/en/best-backup-software-small-business/", sitemap)
        self.assertIn("/fr/meilleur-logiciel-sauvegarde-pme/", sitemap)
        self.assertIn("/es/mejor-software-copias-seguridad-pymes/", sitemap)
        self.assertIn("/de/beste-backup-software-kleine-unternehmen/", sitemap)

    def test_ransomware_recovery_checklist_page_is_generated_with_sources_and_cta(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        page = self.tmpdir / "en" / "ransomware-recovery-checklist-small-business" / "index.html"
        self.assertTrue(page.exists())
        html = page.read_text(encoding="utf-8")
        self.assertIn("Ransomware recovery checklist for small business", html)
        self.assertIn("not incident-response advice", html)
        self.assertIn("Get my stack recommendation", html)
        self.assertIn("https://www.verizon.com/business/resources/reports/dbir/", html)
        self.assertIn("https://www.cisa.gov/stopransomware/ransomware-guide", html)

    def test_robots_and_legal_pages_are_generated(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        self.assertTrue((self.tmpdir / "robots.txt").exists())
        for slug in ["affiliate-disclosure", "privacy-policy", "methodology"]:
            self.assertTrue((self.tmpdir / "en" / slug / "index.html").exists())

    def test_build_supports_github_project_pages_path_prefix(self):
        from src.generate_site import build_site

        build_site(
            self.tmpdir,
            base_url="https://stackshieldadvisor.github.io/stackshield-advisor",
            path_prefix="/stackshield-advisor",
        )

        home = (self.tmpdir / "en" / "index.html").read_text(encoding="utf-8")
        root = (self.tmpdir / "index.html").read_text(encoding="utf-8")
        sitemap = (self.tmpdir / "sitemap.xml").read_text(encoding="utf-8")

        self.assertIn('href="/stackshield-advisor/assets/styles.css"', home)
        self.assertIn('src="/stackshield-advisor/assets/recommender.js"', home)
        self.assertIn('href="/stackshield-advisor/en/best-backup-software-small-business/"', home)
        self.assertIn("url=/stackshield-advisor/en/", root)
        self.assertIn("https://stackshieldadvisor.github.io/stackshield-advisor/en/", sitemap)

    def test_ransomware_recovery_checklist_page_is_generated_and_sourced(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        page_path = self.tmpdir / "en" / "ransomware-recovery-checklist-small-business" / "index.html"
        self.assertTrue(page_path.exists())
        content = page_path.read_text(encoding="utf-8")

        self.assertIn("Ransomware Recovery Checklist for Small Business", content)
        self.assertIn("not incident-response advice", content)
        self.assertIn("CISA", content)
        self.assertIn("NCSC", content)
        self.assertIn("Verizon DBIR", content)
        self.assertIn("https://www.cisa.gov/stopransomware/ransomware-guide", content)
        self.assertIn("https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks", content)
        self.assertIn("/en/small-business-cyber-stack-recommender/", content)

    def test_ransomware_recovery_checklist_is_in_sitemap(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        sitemap = (self.tmpdir / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/en/ransomware-recovery-checklist-small-business/", sitemap)

    def test_nis2_supplier_readiness_page_is_generated_with_sources_and_disclaimer(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        page_path = self.tmpdir / "en" / "nis2-supplier-cybersecurity-readiness-checklist" / "index.html"
        self.assertTrue(page_path.exists())
        content = page_path.read_text(encoding="utf-8")

        self.assertIn("NIS2 Supplier Cybersecurity Readiness Checklist for SMEs", content)
        self.assertIn("not legal advice", content)
        self.assertIn("not a NIS2 applicability assessment", content)
        self.assertIn("European Commission", content)
        self.assertIn("ENISA", content)
        self.assertIn("European DIGITAL SME Alliance", content)
        self.assertIn("https://digital-strategy.ec.europa.eu/en/policies/nis2-directive", content)
        self.assertIn("https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance", content)
        self.assertIn("https://www.digitalsme.eu/digital-sme-launches-guide-to-position-smes-as-trusted-nis2-suppliers/", content)
        self.assertIn("/en/ransomware-recovery-checklist-small-business/", content)

    def test_nis2_supplier_readiness_page_is_in_sitemap(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        sitemap = (self.tmpdir / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/en/nis2-supplier-cybersecurity-readiness-checklist/", sitemap)

    def test_static_google_verification_file_is_copied_to_site_root(self):
        from src.generate_site import build_site

        build_site(self.tmpdir)

        verification = self.tmpdir / "googled641817ccf2647bb.html"
        self.assertTrue(verification.exists())
        self.assertEqual(
            verification.read_text(encoding="utf-8").strip(),
            "google-site-verification: googled641817ccf2647bb.html",
        )


if __name__ == "__main__":
    unittest.main()
