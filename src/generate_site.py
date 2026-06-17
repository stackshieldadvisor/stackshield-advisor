from __future__ import annotations

import html
import os
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SITE_NAME = "StackShield Advisor"
DEFAULT_BASE_URL = "https://stackshieldadvisor.github.io"
LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "es": "Español",
    "de": "Deutsch",
}

AFFILIATE_DISCLOSURE = (
    "Some links on this site may be affiliate links. If you buy through them, "
    "we may earn a commission at no extra cost to you. Recommendations are based "
    "on documented features, public information and stated use cases, not on payment alone. "
    "Sponsored placements are clearly marked."
)

FREE_HOSTING_NOTE = {
    "en": "Designed for free deployment on Cloudflare Pages, GitHub Pages, Netlify or Vercel. No paid domain is required to validate traction.",
    "fr": "Conçu pour un déploiement gratuit sur Cloudflare Pages, GitHub Pages, Netlify ou Vercel. Aucun domaine payant n'est nécessaire pour valider la traction.",
    "es": "Diseñado para despliegue gratuito en Cloudflare Pages, GitHub Pages, Netlify o Vercel. No se necesita dominio de pago para validar la tracción.",
    "de": "Für kostenloses Deployment auf Cloudflare Pages, GitHub Pages, Netlify oder Vercel konzipiert. Eine bezahlte Domain ist zur Validierung nicht nötig.",
}


@dataclass(frozen=True)
class Page:
    lang: str
    slug: str
    title: str
    description: str
    body: str
    commercial: bool = False

    @property
    def path(self) -> str:
        if self.slug:
            return f"/{self.lang}/{self.slug}/"
        return f"/{self.lang}/"


CORE_SLUGS = {
    "home": {"en": "", "fr": "", "es": "", "de": ""},
    "backup": {
        "en": "best-backup-software-small-business",
        "fr": "meilleur-logiciel-sauvegarde-pme",
        "es": "mejor-software-copias-seguridad-pymes",
        "de": "beste-backup-software-kleine-unternehmen",
    },
    "recommender": {
        "en": "small-business-cyber-stack-recommender",
        "fr": "recommandation-cybersecurite-pme",
        "es": "recomendador-ciberseguridad-pymes",
        "de": "cybersecurity-stack-empfehlung-kleine-unternehmen",
    },
    "disclosure": {
        "en": "affiliate-disclosure",
        "fr": "transparence-affiliation",
        "es": "divulgacion-afiliacion",
        "de": "affiliate-offenlegung",
    },
    "privacy": {
        "en": "privacy-policy",
        "fr": "politique-confidentialite",
        "es": "politica-privacidad",
        "de": "datenschutz",
    },
    "methodology": {
        "en": "methodology",
        "fr": "methodologie",
        "es": "metodologia",
        "de": "methodik",
    },
    "ransomware_recovery": {
        "en": "ransomware-recovery-checklist-small-business",
    },
}

TRANSLATIONS = {
    "en": {
        "tagline": "Practical cybersecurity and backup software guidance for small businesses.",
        "hero_title": "Choose a safer small-business cyber stack without drowning in vendor jargon.",
        "hero_sub": "Independent decision pages, checklists and tools for backup, ransomware resilience, password management and email security.",
        "cta_primary": "Get my recommendation",
        "cta_secondary": "Compare backup tools",
        "pill_1": "No email required",
        "pill_2": "Affiliate links disclosed",
        "pill_3": "Built for free-hosted validation",
        "section_title": "Initial focus",
        "section_body": "The first version focuses on backup, ransomware recovery, password managers, MFA and email security for small professional firms.",
        "backup_title": "Best Backup Software for Small Business: a practical decision framework",
        "backup_desc": "A pragmatic guide for choosing backup software for small businesses, with ransomware resilience, recovery objectives and operational risk in mind.",
        "rec_title": "Small Business Cyber Stack Recommender",
        "rec_desc": "A local, no-email tool to identify the minimum security stack a small business should evaluate first.",
    },
    "fr": {
        "tagline": "Guides pratiques pour choisir sauvegarde et cybersécurité en PME.",
        "hero_title": "Choisir une pile cyber plus sûre pour PME sans se noyer dans le jargon vendeur.",
        "hero_sub": "Pages de décision, checklists et outils pour sauvegarde, ransomware, mots de passe et sécurité email.",
        "cta_primary": "Obtenir ma recommandation",
        "cta_secondary": "Comparer les outils de sauvegarde",
        "pill_1": "Sans email obligatoire",
        "pill_2": "Affiliation signalée",
        "pill_3": "Pensé pour hébergement gratuit",
        "section_title": "Focalisation initiale",
        "section_body": "La première version se concentre sur sauvegarde, reprise ransomware, gestionnaires de mots de passe, MFA et sécurité email pour petites structures professionnelles.",
        "backup_title": "Meilleur logiciel de sauvegarde pour PME : cadre de décision pratique",
        "backup_desc": "Guide pragmatique pour choisir un logiciel de sauvegarde pour PME, en tenant compte de la résilience ransomware, des objectifs de reprise et du risque opérationnel.",
        "rec_title": "Recommandation de pile cybersécurité PME",
        "rec_desc": "Outil local, sans email, pour identifier la pile de sécurité minimale qu'une PME devrait évaluer en priorité.",
    },
    "es": {
        "tagline": "Guías prácticas de ciberseguridad y copias de seguridad para pymes.",
        "hero_title": "Elige una pila de ciberseguridad para pymes sin perderte en jerga comercial.",
        "hero_sub": "Páginas de decisión, listas y herramientas para backup, ransomware, contraseñas y seguridad del correo.",
        "cta_primary": "Obtener recomendación",
        "cta_secondary": "Comparar herramientas de backup",
        "pill_1": "Sin email obligatorio",
        "pill_2": "Afiliación declarada",
        "pill_3": "Preparado para hosting gratuito",
        "section_title": "Enfoque inicial",
        "section_body": "La primera versión se centra en backup, recuperación ante ransomware, gestores de contraseñas, MFA y seguridad de email para pequeñas empresas profesionales.",
        "backup_title": "Mejor software de copias de seguridad para pymes: marco práctico de decisión",
        "backup_desc": "Guía pragmática para elegir software de backup para pymes, considerando resiliencia ante ransomware, objetivos de recuperación y riesgo operativo.",
        "rec_title": "Recomendador de pila de ciberseguridad para pymes",
        "rec_desc": "Herramienta local, sin email, para identificar la pila mínima de seguridad que una pyme debería evaluar primero.",
    },
    "de": {
        "tagline": "Praktische Cybersecurity- und Backup-Guides für kleine Unternehmen.",
        "hero_title": "Wähle einen sichereren Cyber-Stack für kleine Unternehmen ohne Vendor-Jargon.",
        "hero_sub": "Entscheidungsseiten, Checklisten und Tools für Backup, Ransomware-Resilienz, Passwortmanagement und E-Mail-Sicherheit.",
        "cta_primary": "Empfehlung erhalten",
        "cta_secondary": "Backup-Tools vergleichen",
        "pill_1": "Keine E-Mail erforderlich",
        "pill_2": "Affiliate-Links offengelegt",
        "pill_3": "Für kostenloses Hosting gebaut",
        "section_title": "Erster Fokus",
        "section_body": "Die erste Version fokussiert Backup, Ransomware-Recovery, Passwortmanager, MFA und E-Mail-Sicherheit für kleine professionelle Unternehmen.",
        "backup_title": "Beste Backup-Software für kleine Unternehmen: ein praktischer Entscheidungsrahmen",
        "backup_desc": "Pragmatischer Leitfaden zur Auswahl von Backup-Software für kleine Unternehmen mit Fokus auf Ransomware-Resilienz, Recovery-Ziele und operatives Risiko.",
        "rec_title": "Cybersecurity-Stack-Empfehlung für kleine Unternehmen",
        "rec_desc": "Lokales Tool ohne E-Mail, um den minimalen Security-Stack zu identifizieren, den ein kleines Unternehmen zuerst prüfen sollte.",
    },
}


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def normalize_path_prefix(path_prefix: str | None) -> str:
    if not path_prefix:
        return ""
    cleaned = path_prefix.strip()
    if not cleaned or cleaned == "/":
        return ""
    return "/" + cleaned.strip("/")


def prefixed(path_prefix: str, path: str) -> str:
    normalized = normalize_path_prefix(path_prefix)
    if not normalized:
        return path
    if not path.startswith("/"):
        path = "/" + path
    return normalized + path


def apply_path_prefix(html_text: str, path_prefix: str) -> str:
    normalized = normalize_path_prefix(path_prefix)
    if not normalized:
        return html_text
    return (
        html_text
        .replace('href="/', f'href="{normalized}/')
        .replace("href='/", f"href='{normalized}/")
        .replace('src="/', f'src="{normalized}/')
        .replace("src='/", f"src='{normalized}/")
        .replace('url=/', f'url={normalized}/')
    )


def canonical(base_url: str, page: Page) -> str:
    return base_url.rstrip("/") + page.path


def alternate_links(base_url: str, pages_by_key: dict[str, dict[str, Page]], key: str) -> str:
    links = []
    lang_pages = pages_by_key[key]
    for lang in LANGUAGES:
        page = lang_pages.get(lang)
        if page is None:
            continue
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{canonical(base_url, page)}">')
    default_page = lang_pages.get("en") or next(iter(lang_pages.values()))
    links.append(f'<link rel="alternate" hreflang="x-default" href="{canonical(base_url, default_page)}">')
    return "\n    ".join(links)


def layout(page: Page, key: str, pages_by_key: dict[str, dict[str, Page]], base_url: str, path_prefix: str = "") -> str:
    current_url = canonical(base_url, page)
    lang_nav = " · ".join(
        f'<a href="{pages_by_key[key][lang].path}">{label}</a>'
        for lang, label in LANGUAGES.items()
        if lang in pages_by_key[key]
    )
    disclosure = ""
    if page.commercial:
        disclosure = f"""
        <aside class="disclosure" aria-label="Affiliate disclosure">
          <strong>Affiliate disclosure</strong><br>{escape(AFFILIATE_DISCLOSURE)}
        </aside>
        """
    html_text = f"""<!doctype html>
<html lang="{page.lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page.title)} · {SITE_NAME}</title>
  <meta name="description" content="{escape(page.description)}">
  <link rel="canonical" href="{current_url}">
  {alternate_links(base_url, pages_by_key, key)}
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/{page.lang}/" aria-label="{SITE_NAME} home">
      <span class="brand-mark">S</span><span>{SITE_NAME}</span>
    </a>
    <nav class="main-nav">
      <a href="/{page.lang}/{CORE_SLUGS['backup'][page.lang]}/">Backup</a>
      <a href="/{page.lang}/{CORE_SLUGS['recommender'][page.lang]}/">Recommender</a>
      <a href="/{page.lang}/{CORE_SLUGS['methodology'][page.lang]}/">Methodology</a>
    </nav>
  </header>
  <main class="container">
    {disclosure}
    {page.body}
    <section class="language-switcher" aria-label="Language switcher">
      <strong>Languages:</strong> {lang_nav}
    </section>
  </main>
  <footer class="site-footer">
    <p>© {date.today().year} {SITE_NAME}. Anonymous, source-based software guidance. Not legal, financial, medical or incident-response advice.</p>
    <p><a href="/{page.lang}/{CORE_SLUGS['disclosure'][page.lang]}/">Affiliate disclosure</a> · <a href="/{page.lang}/{CORE_SLUGS['privacy'][page.lang]}/">Privacy</a> · <a href="/{page.lang}/{CORE_SLUGS['methodology'][page.lang]}/">Methodology</a></p>
  </footer>
  <script src="/assets/recommender.js" defer></script>
</body>
</html>"""
    return apply_path_prefix(html_text, path_prefix)


def home_body(lang: str) -> str:
    t = TRANSLATIONS[lang]
    return f"""
    <section class="hero">
      <p class="eyebrow">{escape(t['tagline'])}</p>
      <h1>{escape(t['hero_title'])}</h1>
      <p class="lede">{escape(t['hero_sub'])}</p>
      <div class="cta-row">
        <a class="button primary" href="/{lang}/{CORE_SLUGS['recommender'][lang]}/">{escape(t['cta_primary'])}</a>
        <a class="button secondary" href="/{lang}/{CORE_SLUGS['backup'][lang]}/">{escape(t['cta_secondary'])}</a>
      </div>
      <div class="pills"><span>{escape(t['pill_1'])}</span><span>{escape(t['pill_2'])}</span><span>{escape(t['pill_3'])}</span></div>
    </section>
    <section class="grid two">
      <article class="card">
        <h2>{escape(t['section_title'])}</h2>
        <p>{escape(t['section_body'])}</p>
      </article>
      <article class="card">
        <h2>Free validation first</h2>
        <p>{escape(FREE_HOSTING_NOTE[lang])}</p>
      </article>
    </section>
    <section>
      <h2>Initial commercial pages</h2>
      <ul class="link-list">
        <li><a href="/{lang}/{CORE_SLUGS['backup'][lang]}/">Backup software decision framework</a></li>
        <li><a href="/{lang}/{CORE_SLUGS['recommender'][lang]}/">Small-business cyber stack recommender</a></li>
      </ul>
    </section>
    """


def backup_body(lang: str) -> str:
    t = TRANSLATIONS[lang]
    return f"""
    <article class="article">
      <p class="eyebrow">Backup · ransomware resilience · small business</p>
      <h1>{escape(t['backup_title'])}</h1>
      <p class="lede">{escape(t['backup_desc'])}</p>
      <section class="decision-box">
        <h2>Cold recommendation</h2>
        <p>Choose backup software by recovery reliability first, interface second, and price third. A cheap backup that cannot restore fast after ransomware is not a backup strategy.</p>
      </section>
      <section>
        <h2>Decision matrix</h2>
        <table>
          <thead><tr><th>Criterion</th><th>Why it matters</th><th>Minimum acceptable signal</th></tr></thead>
          <tbody>
            <tr><td>Immutable backups</td><td>Limits ransomware damage.</td><td>Vendor documents immutability, object lock, or tamper-resistant retention.</td></tr>
            <tr><td>Recovery testing</td><td>Backups are worthless if restores fail.</td><td>Clear restore workflow and test schedule.</td></tr>
            <tr><td>RTO/RPO fit</td><td>Matches tolerated downtime and data loss.</td><td>Business can define target recovery time and recovery point.</td></tr>
            <tr><td>MFA and role control</td><td>Backup consoles are high-value targets.</td><td>MFA available for administrators.</td></tr>
            <tr><td>Device and SaaS coverage</td><td>Small firms often mix laptops, cloud drives and Microsoft/Google accounts.</td><td>Covers the systems actually used.</td></tr>
          </tbody>
        </table>
      </section>
      <section>
        <h2>Starter shortlist categories</h2>
        <p>This first prototype does not rank vendors yet. Vendor pages will only be published after public evidence is collected for features, pricing model and affiliate status.</p>
        <ul>
          <li>Cloud backup for endpoints</li>
          <li>Microsoft 365 / Google Workspace backup</li>
          <li>NAS and local image backup</li>
          <li>Managed backup through MSP/MSSP</li>
        </ul>
      </section>
      <section class="cta-panel">
        <h2>Next step</h2>
        <p>Use the recommender to identify the minimum stack to evaluate before comparing vendors.</p>
        <a class="button primary" href="/{lang}/{CORE_SLUGS['recommender'][lang]}/">Get my recommendation</a>
      </section>
    </article>
    """


def recommender_body(lang: str) -> str:
    t = TRANSLATIONS[lang]
    return f"""
    <article class="article">
      <p class="eyebrow">Local tool · No email required</p>
      <h1>{escape(t['rec_title'])}</h1>
      <p class="lede">{escape(t['rec_desc'])}</p>
      <form id="stack-recommender" class="tool-card">
        <label>Business size
          <select name="size">
            <option value="solo">Solo / 1–2 people</option>
            <option value="small">3–20 people</option>
            <option value="growing">21–100 people</option>
          </select>
        </label>
        <label>Primary risk
          <select name="risk">
            <option value="ransomware">Ransomware / data loss</option>
            <option value="phishing">Phishing / email compromise</option>
            <option value="compliance">Client or supplier cybersecurity pressure</option>
          </select>
        </label>
        <label>Internal IT capacity
          <select name="it">
            <option value="none">No dedicated IT</option>
            <option value="part_time">Part-time IT or technical founder</option>
            <option value="team">Internal IT team</option>
          </select>
        </label>
        <button class="button primary" type="submit">Get my recommendation</button>
        <p class="microcopy">No email required. This tool runs in your browser and does not submit personal data.</p>
      </form>
      <section id="recommendation-output" class="result-box" hidden></section>
    </article>
    """


def ransomware_recovery_body() -> str:
    return """
    <article class="article">
      <p class="eyebrow">Ransomware recovery · backup readiness · small business</p>
      <h1>Ransomware Recovery Checklist for Small Business</h1>
      <p class="lede">A practical, source-backed checklist for choosing and operating backups before a ransomware incident turns into prolonged downtime.</p>

      <section class="decision-box">
        <h2>Cold recommendation</h2>
        <p>If your business is currently under attack, do not use this page as a response runbook. Isolate affected systems, preserve evidence where possible, contact qualified incident-response support, notify your insurer or legal counsel if relevant, and report cyber-enabled crime through the appropriate official channels. This page is planning guidance, not incident-response advice.</p>
      </section>

      <section>
        <h2>What “ransomware recovery” means</h2>
        <p>For a small business, ransomware recovery is the ability to restore critical operations, files, identities and cloud data after systems are encrypted, deleted, locked or exfiltrated. CISA defines ransomware as malware designed to encrypt files and make systems unusable until a ransom is demanded; it also notes that modern cases may include data theft and extortion.</p>
        <p>The practical objective is not “perfect security”. It is to keep one clean recovery path available when laptops, servers, cloud accounts or backup consoles are compromised.</p>
      </section>

      <section>
        <h2>Decision matrix before buying backup software</h2>
        <table>
          <thead><tr><th>Criterion</th><th>Why it matters</th><th>Minimum small-business signal</th><th>Red flag</th></tr></thead>
          <tbody>
            <tr><td>Offline or immutable backup copy</td><td>CISA recommends maintaining offline, encrypted backups and regularly testing backup availability and integrity. Ransomware often attempts to delete or encrypt reachable backups.</td><td>At least one backup copy is offline, immutable, object-locked or otherwise tamper-resistant.</td><td>All backups are always mounted with normal admin credentials.</td></tr>
            <tr><td>Restore testing</td><td>A backup is only useful if the business can restore from it under pressure.</td><td>A documented monthly or quarterly restore test for one real file, one SaaS account and one critical system.</td><td>The vendor shows backup status but no clear restore workflow.</td></tr>
            <tr><td>RTO and RPO fit</td><td>RTO is the target recovery time. RPO is the maximum acceptable data loss window. They turn “we need backups” into a business decision.</td><td>Management has written the maximum tolerable downtime and data loss for each critical process.</td><td>Every system is treated as equally critical, so nothing is prioritized.</td></tr>
            <tr><td>Administrator MFA</td><td>Backup consoles are high-value targets because an attacker who controls them may delete recovery points.</td><td>Multi-factor authentication is enforced for every administrator and recovery action is logged.</td><td>Shared admin account, no MFA, or no audit trail.</td></tr>
            <tr><td>SaaS and identity coverage</td><td>Small firms often depend on Microsoft 365, Google Workspace, cloud drives and identity providers, not just laptops.</td><td>The backup scope explicitly includes the systems where contracts, invoices, client files and email live.</td><td>Endpoint backup is purchased while critical SaaS data is excluded.</td></tr>
            <tr><td>Response handoff</td><td>CISA and the FBI emphasize coordinated response and reporting. Backup restore should not erase evidence or worsen compromise.</td><td>The business knows who can authorize shutdown, restoration, reporting and external support.</td><td>No written escalation owner outside the compromised IT account.</td></tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>One-page readiness checklist</h2>
        <h3>Before an incident</h3>
        <ul>
          <li>List the five systems the business cannot operate without: email, accounting, client files, production system, website or booking system.</li>
          <li>Write an RTO and RPO for each system. Example: “accounting restored within 24 hours; maximum one business day of data loss”.</li>
          <li>Keep at least one backup path that ransomware cannot normally modify: offline, immutable or strongly access-controlled.</li>
          <li>Enable MFA on backup, identity, email, finance and admin accounts.</li>
          <li>Run a restore test and record date, owner, duration, failure points and next correction.</li>
          <li>Store recovery instructions outside the normal network: printed, offline or in a separate protected vault.</li>
        </ul>
        <h3>If ransomware is suspected</h3>
        <ul>
          <li>Do not rush to restore over compromised systems without expert review.</li>
          <li>Escalate to the named decision owner and qualified incident-response support if available.</li>
          <li>Preserve logs and affected devices where possible; restoration can destroy useful evidence.</li>
          <li>Use official reporting routes where applicable. The FBI asks victims of internet crime to submit complaints to IC3 and contact law enforcement.</li>
        </ul>
        <h3>After restoration</h3>
        <ul>
          <li>Reset credentials and review administrative access before reconnecting restored systems.</li>
          <li>Patch the exploited entry point if known. Verizon’s 2026 DBIR highlights software vulnerabilities as a leading breach entry point.</li>
          <li>Run a lessons-learned review: what failed, what restored, what must be changed before the next test.</li>
        </ul>
      </section>

      <section>
        <h2>Fast scoring rule</h2>
        <p>Score each line from 0 to 2. A business below 7/12 should not spend time comparing vendor brands yet; it should fix requirements first.</p>
        <table>
          <thead><tr><th>Control</th><th>0</th><th>1</th><th>2</th></tr></thead>
          <tbody>
            <tr><td>Critical systems listed</td><td>No list</td><td>Partial list</td><td>Owner-approved list</td></tr>
            <tr><td>RTO/RPO defined</td><td>No</td><td>Informal</td><td>Written by process</td></tr>
            <tr><td>Tamper-resistant backup</td><td>No</td><td>Some coverage</td><td>Critical data covered</td></tr>
            <tr><td>Restore test</td><td>Never tested</td><td>Test older than 90 days</td><td>Recent documented test</td></tr>
            <tr><td>Admin MFA</td><td>No</td><td>Some admins</td><td>All admins enforced</td></tr>
            <tr><td>Escalation owner</td><td>No owner</td><td>Informal owner</td><td>Named owner and backup owner</td></tr>
          </tbody>
        </table>
      </section>

      <section class="cta-panel">
        <h2>Next step</h2>
        <p>Use the StackShield recommender to identify the minimum security stack to evaluate before comparing backup vendors.</p>
        <a class="button primary" href="/en/small-business-cyber-stack-recommender/">Get my stack recommendation</a>
      </section>

      <section>
        <h2>Sources and limits</h2>
        <ul>
          <li>CISA, #StopRansomware Guide: recommends offline encrypted backups, restore testing, incident-response planning and coordinated response. <a href="https://www.cisa.gov/stopransomware/ransomware-guide">https://www.cisa.gov/stopransomware/ransomware-guide</a></li>
          <li>NCSC, Mitigating malware and ransomware attacks: emphasizes recent offline backups, restore knowledge, regular restoration testing, and defence-in-depth. <a href="https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks">https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks</a></li>
          <li>NCSC, Offline backups in an online world: explains why at least one backup should remain offline or logically disconnected, and describes the 3-2-1 backup rule. <a href="https://www.ncsc.gov.uk/blog-post/offline-backups-in-an-online-world">https://www.ncsc.gov.uk/blog-post/offline-backups-in-an-online-world</a></li>
          <li>Verizon DBIR, 2026 Data Breach Investigations Report: ransomware is listed as involving 48% of breaches, and software vulnerabilities as 31% of breach entry points. <a href="https://www.verizon.com/business/resources/reports/dbir/">https://www.verizon.com/business/resources/reports/dbir/</a></li>
          <li>FBI, 2024 Internet Crime Report press release: 859,532 complaints and reported losses exceeding $16 billion in 2024; phishing/spoofing, extortion and personal data breaches were the top three categories by complaint count. <a href="https://www.fbi.gov/news/press-releases/fbi-releases-annual-internet-crime-report">https://www.fbi.gov/news/press-releases/fbi-releases-annual-internet-crime-report</a></li>
        </ul>
        <p><strong>Disclaimer:</strong> this is educational planning material for small-business resilience. It is not legal advice, insurance advice, forensic advice or ransomware incident-response advice.</p>
      </section>
    </article>
    """


def legal_body(kind: str, lang: str) -> tuple[str, str, str]:
    titles = {
        "disclosure": "Affiliate disclosure",
        "privacy": "Privacy policy",
        "methodology": "Methodology",
    }
    if kind == "disclosure":
        body = f"""
        <article class="article"><h1>Affiliate disclosure</h1>
        <p>{escape(AFFILIATE_DISCLOSURE)}</p>
        <p>We do not publish fake reviews. Sponsored placements must be explicitly marked. Payment alone must not determine the recommendation.</p>
        </article>
        """
        return titles[kind], "How StackShield Advisor discloses affiliate relationships and sponsored placements.", body
    if kind == "privacy":
        body = """
        <article class="article"><h1>Privacy policy</h1>
        <p>This prototype is designed to avoid collecting personal data by default. The recommender runs locally in the browser and does not require an email address.</p>
        <p>If forms, newsletters or lead-transfer features are added later, they must include clear consent, data minimisation, retention limits and a simple withdrawal route.</p>
        </article>
        """
        return titles[kind], "Privacy principles for a no-email prototype and future compliant lead collection.", body
    body = """
    <article class="article"><h1>Methodology</h1>
    <p>Pages are built from public vendor information, documented features, pricing pages where available, user-fit criteria and transparent commercial disclosures.</p>
    <p>Claims should be sourced. If evidence is missing or uncertain, the page must say so rather than invent certainty.</p>
    <p>This site is not legal advice, cybersecurity incident-response advice, financial advice or a replacement for a qualified professional assessment.</p>
    </article>
    """
    return titles[kind], "How StackShield Advisor evaluates software categories and limits claims.", body


def build_pages() -> tuple[list[Page], dict[str, dict[str, Page]]]:
    pages: list[Page] = []
    pages_by_key: dict[str, dict[str, Page]] = {key: {} for key in CORE_SLUGS}
    for lang in LANGUAGES:
        home = Page(lang, "", SITE_NAME, TRANSLATIONS[lang]["tagline"], home_body(lang))
        backup = Page(lang, CORE_SLUGS["backup"][lang], TRANSLATIONS[lang]["backup_title"], TRANSLATIONS[lang]["backup_desc"], backup_body(lang), commercial=True)
        recommender = Page(lang, CORE_SLUGS["recommender"][lang], TRANSLATIONS[lang]["rec_title"], TRANSLATIONS[lang]["rec_desc"], recommender_body(lang), commercial=True)
        pages_by_key["home"][lang] = home
        pages_by_key["backup"][lang] = backup
        pages_by_key["recommender"][lang] = recommender
        pages.extend([home, backup, recommender])
        for kind in ["disclosure", "privacy", "methodology"]:
            title, desc, body = legal_body(kind, lang)
            page = Page(lang, CORE_SLUGS[kind][lang], title, desc, body)
            pages_by_key[kind][lang] = page
            pages.append(page)
    ransomware_recovery = Page(
        "en",
        CORE_SLUGS["ransomware_recovery"]["en"],
        "Ransomware recovery checklist for small business",
        "A source-backed ransomware recovery and backup readiness checklist for small businesses, with RTO/RPO, restore testing, immutable backup and admin MFA criteria.",
        ransomware_recovery_body(),
        commercial=True,
    )
    pages_by_key["ransomware_recovery"]["en"] = ransomware_recovery
    pages.append(ransomware_recovery)
    return pages, pages_by_key


def write_page(output_dir: Path, page: Page, key: str, pages_by_key: dict[str, dict[str, Page]], base_url: str, path_prefix: str = "") -> None:
    page_dir = output_dir / page.lang / page.slug if page.slug else output_dir / page.lang
    page_dir.mkdir(parents=True, exist_ok=True)
    (page_dir / "index.html").write_text(layout(page, key, pages_by_key, base_url, path_prefix), encoding="utf-8")


def write_assets(output_dir: Path) -> None:
    assets = output_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "styles.css").write_text(STYLES, encoding="utf-8")
    (assets / "recommender.js").write_text(RECOMMENDER_JS, encoding="utf-8")


def write_static_files(output_dir: Path) -> None:
    static_dir = Path(__file__).resolve().parents[1] / "static"
    if not static_dir.exists():
        return
    for source in static_dir.rglob("*"):
        if source.is_file():
            destination = output_dir / source.relative_to(static_dir)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def write_sitemap(output_dir: Path, pages: list[Page], base_url: str) -> None:
    urls = "\n".join(
        f"  <url><loc>{canonical(base_url, page)}</loc></url>" for page in pages
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    (output_dir / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots(output_dir: Path, base_url: str) -> None:
    (output_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_root_redirect(output_dir: Path, path_prefix: str = "") -> None:
    target = prefixed(path_prefix, "/en/")
    (output_dir / "index.html").write_text(
        f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={target}"><meta name="viewport" content="width=device-width, initial-scale=1"><title>StackShield Advisor</title></head><body><p><a href="{target}">Continue to StackShield Advisor</a></p></body></html>""",
        encoding="utf-8",
    )


def build_site(output_dir: str | Path, base_url: str | None = None, path_prefix: str | None = None) -> Path:
    output_dir = Path(output_dir)
    path_prefix = normalize_path_prefix(path_prefix or os.getenv("SITE_PATH_PREFIX", ""))
    base_url = base_url or os.getenv("SITE_BASE_URL", DEFAULT_BASE_URL)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pages, pages_by_key = build_pages()
    for key, lang_pages in pages_by_key.items():
        for page in lang_pages.values():
            write_page(output_dir, page, key, pages_by_key, base_url, path_prefix)
    write_assets(output_dir)
    write_static_files(output_dir)
    write_sitemap(output_dir, pages, base_url)
    write_robots(output_dir, base_url)
    write_root_redirect(output_dir, path_prefix)
    return output_dir


STYLES = """
:root { color-scheme: light; --bg:#f6f7fb; --ink:#111827; --muted:#5b6472; --card:#ffffff; --line:#d9deea; --accent:#165dff; --accent2:#091a3a; --good:#0f766e; }
* { box-sizing: border-box; }
body { margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:var(--bg); color:var(--ink); line-height:1.55; }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
.site-header { position:sticky; top:0; z-index:10; background:rgba(246,247,251,.92); backdrop-filter: blur(10px); border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; padding:16px clamp(18px,4vw,56px); }
.brand { display:flex; gap:10px; align-items:center; font-weight:800; color:var(--ink); }
.brand-mark { display:inline-grid; place-items:center; width:32px; height:32px; border-radius:10px; color:#fff; background:linear-gradient(135deg, var(--accent2), var(--accent)); }
.main-nav { display:flex; gap:18px; flex-wrap:wrap; font-size:14px; }
.container { max-width:1120px; margin:0 auto; padding:42px 20px 64px; }
.hero { padding:56px clamp(20px,5vw,72px); background:radial-gradient(circle at top left, #dce7ff, transparent 42%), var(--card); border:1px solid var(--line); border-radius:28px; box-shadow:0 18px 60px rgba(17,24,39,.06); }
.eyebrow { color:var(--good); text-transform:uppercase; letter-spacing:.11em; font-size:12px; font-weight:800; }
h1 { font-size:clamp(36px,6vw,68px); line-height:1.02; margin:12px 0 18px; letter-spacing:-.045em; }
h2 { font-size:clamp(24px,3vw,34px); line-height:1.1; letter-spacing:-.025em; }
.lede { font-size:clamp(18px,2vw,22px); color:var(--muted); max-width:780px; }
.cta-row { display:flex; gap:14px; flex-wrap:wrap; margin-top:28px; }
.button { display:inline-flex; align-items:center; justify-content:center; border-radius:999px; padding:12px 18px; font-weight:800; border:1px solid var(--line); }
.button.primary { background:var(--accent); color:white; border-color:var(--accent); }
.button.secondary { background:white; color:var(--accent2); }
.pills { display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }
.pills span { background:#eef3ff; color:#193466; border:1px solid #ccd9ff; padding:8px 12px; border-radius:999px; font-size:14px; font-weight:700; }
.grid.two { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; margin-top:24px; }
.card, .article, .disclosure, .tool-card, .result-box, .decision-box, .cta-panel { background:var(--card); border:1px solid var(--line); border-radius:22px; padding:24px; box-shadow:0 12px 36px rgba(17,24,39,.04); }
.article { margin-top:10px; }
.disclosure { border-color:#f5c46b; background:#fff8e6; margin-bottom:18px; }
table { width:100%; border-collapse:collapse; margin:16px 0; background:white; border-radius:16px; overflow:hidden; }
th, td { border:1px solid var(--line); padding:12px; vertical-align:top; text-align:left; }
th { background:#eef3ff; }
.link-list li { margin:10px 0; }
.tool-card { display:grid; gap:16px; max-width:720px; }
label { display:grid; gap:7px; font-weight:800; }
select { padding:11px 12px; border:1px solid var(--line); border-radius:12px; background:white; font:inherit; }
.microcopy { color:var(--muted); font-size:14px; }
.result-box { margin-top:18px; border-color:#96d6c9; background:#effcf9; }
.language-switcher { margin-top:28px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); }
.site-footer { border-top:1px solid var(--line); padding:28px 20px; text-align:center; color:var(--muted); font-size:14px; }
@media (max-width:760px) { .site-header { align-items:flex-start; flex-direction:column; gap:12px; } .grid.two { grid-template-columns:1fr; } h1 { font-size:38px; } }
"""

RECOMMENDER_JS = """
(function () {
  const form = document.getElementById('stack-recommender');
  const output = document.getElementById('recommendation-output');
  if (!form || !output) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    const size = data.get('size');
    const risk = data.get('risk');
    const it = data.get('it');

    const recommendations = [];
    recommendations.push('Password manager with enforced MFA for administrators');
    recommendations.push('Cloud backup with tested restore workflow');

    if (risk === 'ransomware') {
      recommendations.push('Immutable or tamper-resistant backup retention');
      recommendations.push('Documented ransomware recovery runbook');
    }
    if (risk === 'phishing') {
      recommendations.push('Email security / anti-phishing layer');
      recommendations.push('Security awareness training for staff');
    }
    if (risk === 'compliance') {
      recommendations.push('Basic asset inventory and supplier security documentation');
      recommendations.push('Policy templates for access control, backup and incident escalation');
    }
    if (size === 'growing' || it === 'team') {
      recommendations.push('Endpoint protection with central management');
      recommendations.push('Role-based access and admin activity logging');
    }
    if (it === 'none') {
      recommendations.push('Consider a managed service provider for setup and recovery testing');
    }

    output.hidden = false;
    output.innerHTML = '<h2>Recommended first evaluation stack</h2><ol>' + recommendations.map(item => '<li>' + item + '</li>').join('') + '</ol><p><strong>Next:</strong> compare vendors only after these requirements are clear. This is informational guidance, not incident-response or legal advice.</p>';
  });
})();
"""


if __name__ == "__main__":
    target = Path(os.getenv("SITE_OUTPUT", "dist"))
    build_site(target)
    print(f"Built {SITE_NAME} into {target.resolve()}")
