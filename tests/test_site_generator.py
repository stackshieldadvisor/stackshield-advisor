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

        homepage = (self.tmpdir / "en" / "index.html").read_text(encoding="utf-8")
        sitemap = (self.tmpdir / "sitemap.xml").read_text(encoding="utf-8")
        robots = (self.tmpdir / "robots.txt").read_text(encoding="utf-8")

        self.assertIn('href="/stackshield-advisor/assets/styles.css"', homepage)
        self.assertIn('href="/stackshield-advisor/en/best-backup-software-small-business/"', homepage)
        self.assertIn('href="https://stackshieldadvisor.github.io/stackshield-advisor/en/"', homepage)
        self.assertIn("https://stackshieldadvisor.github.io/stackshield-advisor/en/best-backup-software-small-business/", sitemap)
        self.assertIn("Sitemap: https://stackshieldadvisor.github.io/stackshield-advisor/sitemap.xml", robots)


if __name__ == "__main__":
    unittest.main()
