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
    "rto_rpo_calculator": {
        "en": "rto-rpo-calculator-small-business",
    },
    "nis2_supplier_readiness": {
        "en": "nis2-supplier-cybersecurity-readiness-checklist",
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
    resource_links = [
        f'        <li><a href="/{lang}/{CORE_SLUGS["backup"][lang]}/">Backup software decision framework</a></li>',
        f'        <li><a href="/{lang}/{CORE_SLUGS["recommender"][lang]}/">Small-business cyber stack recommender</a></li>',
    ]
    if lang == "en":
        resource_links.extend([
            f'        <li><a href="/en/{CORE_SLUGS["ransomware_recovery"]["en"]}/">Ransomware recovery checklist</a></li>',
            f'        <li><a href="/en/{CORE_SLUGS["rto_rpo_calculator"]["en"]}/">RTO/RPO calculator for small business</a></li>',
            f'        <li><a href="/en/{CORE_SLUGS["nis2_supplier_readiness"]["en"]}/">NIS2 supplier readiness checklist</a></li>',
        ])
    resource_link_items = "\n".join(resource_links)
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
{resource_link_items}
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
        <p>Define RTO/RPO targets first, then use the StackShield recommender to identify the minimum security stack to evaluate before comparing backup vendors.</p>
        <div class="cta-row">
          <a class="button primary" href="/en/rto-rpo-calculator-small-business/">Calculate RTO/RPO targets</a>
          <a class="button secondary" href="/en/small-business-cyber-stack-recommender/">Get my stack recommendation</a>
        </div>
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


def rto_rpo_calculator_body() -> str:
    return """
    <article class="article">
      <p class="eyebrow">RTO · RPO · backup planning · local tool</p>
      <h1>RTO/RPO Calculator for Small Business</h1>
      <p class="lede">A browser-only estimator that turns tolerated downtime and data-loss windows into practical backup and recovery requirements before vendor comparison.</p>

      <section class="decision-box">
        <h2>Cold recommendation</h2>
        <p>Do not buy backup software until the business has written at least one recovery time objective and one recovery point objective for each critical process. This calculator is a planning aid, not a service-level agreement, legal opinion, insurance assessment or incident-response runbook.</p>
      </section>

      <section>
        <h2>What the calculator estimates</h2>
        <p>NIST defines recovery time objective (RTO) as the length of time an information system can be in recovery before it harms mission or business processes. NIST defines recovery point objective (RPO) as the point in time to which data must be recovered after an outage.</p>
        <p>In plain terms: RTO asks “how long can this be down?” RPO asks “how much recent data can we afford to lose or recreate?” Ready.gov recommends setting IT recovery priorities and recovery time objectives during the business impact analysis, then matching IT recovery time to the business function that depends on it.</p>
      </section>

      <form id="rto-rpo-calculator" class="tool-card">
        <label>Critical process
          <select name="process">
            <option value="email">Email and calendar</option>
            <option value="finance">Accounting, billing or payroll</option>
            <option value="client_files">Client files or project delivery</option>
            <option value="production">Production, booking or revenue system</option>
            <option value="identity">Identity, admin or password vault</option>
          </select>
        </label>
        <label>Maximum tolerable downtime in hours (RTO target)
          <input name="downtime" type="number" min="0.25" step="0.25" value="24" required>
        </label>
        <label>Maximum acceptable data loss in hours (RPO target)
          <input name="data_loss" type="number" min="0" step="0.25" value="24" required>
        </label>
        <label>People unable to work if this process is unavailable
          <input name="people" type="number" min="0" step="1" value="5">
        </label>
        <label>Estimated loaded cost per blocked person-hour, in your currency (optional)
          <input name="hourly_cost" type="number" min="0" step="1" value="50">
        </label>
        <label>Manual workaround
          <select name="workaround">
            <option value="none">No reliable workaround</option>
            <option value="partial">Partial workaround exists</option>
            <option value="strong">Tested workaround exists</option>
          </select>
        </label>
        <button class="button primary" type="submit">Estimate recovery tier</button>
        <p class="microcopy">No email required. The calculation runs locally in your browser and does not submit business data.</p>
      </form>
      <section id="rto-rpo-output" class="result-box" hidden></section>

      <section>
        <h2>How to interpret the result</h2>
        <table>
          <thead><tr><th>Result pattern</th><th>Practical implication before buying</th><th>Vendor evidence to request</th></tr></thead>
          <tbody>
            <tr><td>RTO under 4 hours or RPO under 1 hour</td><td>This is a critical recovery tier. Manual restore and ad hoc local backup are unlikely to be enough.</td><td>Documented restore workflow, frequent recovery points, admin MFA, immutable or strongly protected retention, and support model.</td></tr>
            <tr><td>RTO within 24 hours and RPO within 24 hours</td><td>This is a standard business-critical tier for many small firms, but it still requires automation and restore testing.</td><td>Daily or more frequent backup, restore-test procedure, SaaS coverage, retention policy and audit trail.</td></tr>
            <tr><td>RTO above 72 hours and RPO above 48 hours</td><td>This may be acceptable only for non-critical processes with a tested workaround.</td><td>Clear scope boundaries, low-cost retention, documented exclusions and a reason why slower restore is acceptable.</td></tr>
          </tbody>
        </table>
      </section>

      <section class="cta-panel">
        <h2>Next step</h2>
        <p>Use the ransomware recovery checklist to turn the RTO/RPO targets into backup, restore-test, MFA and escalation requirements.</p>
        <a class="button primary" href="/en/ransomware-recovery-checklist-small-business/">Use the ransomware recovery checklist</a>
      </section>

      <section>
        <h2>Sources and limits</h2>
        <ul>
          <li>NIST CSRC Glossary, Recovery Time Objective: definition sourced from NIST SP 800-34 Rev. 1. <a href="https://csrc.nist.gov/glossary/term/recovery_time_objective">https://csrc.nist.gov/glossary/term/recovery_time_objective</a></li>
          <li>NIST CSRC Glossary, RPO: “the point in time to which data must be recovered after an outage.” <a href="https://csrc.nist.gov/glossary/term/rpo">https://csrc.nist.gov/glossary/term/rpo</a></li>
          <li>Ready.gov, IT Disaster Recovery Plan: states that IT recovery priorities and recovery time objectives should be developed during business impact analysis and that plans should be periodically tested. <a href="https://www.ready.gov/business/emergency-plans/recovery-plan">https://www.ready.gov/business/emergency-plans/recovery-plan</a></li>
          <li>CISA, #StopRansomware Guide: recommends offline, encrypted backups of critical data and regular testing of backup availability and integrity. <a href="https://www.cisa.gov/stopransomware/ransomware-guide">https://www.cisa.gov/stopransomware/ransomware-guide</a></li>
        </ul>
        <p><strong>Disclaimer:</strong> this tool gives a rough planning estimate. Actual recovery capability depends on architecture, contracts, restore tests, identity security, data scope, incident conditions and supplier performance.</p>
      </section>
    </article>
    """


def nis2_supplier_readiness_body() -> str:
    return """
    <article class="article">
      <p class="eyebrow">NIS2 supplier readiness · SME cybersecurity evidence · Europe</p>
      <h1>NIS2 Supplier Cybersecurity Readiness Checklist for SMEs</h1>
      <p class="lede">A non-legal checklist for small and medium-sized suppliers that need to answer client cybersecurity questionnaires or show basic resilience to organisations affected by NIS2.</p>

      <section class="decision-box">
        <h2>Cold recommendation</h2>
        <p>Do not start by claiming “NIS2 compliant”. Start by preparing a small evidence pack: what systems you use, who can access them, how backups are protected, how incidents are escalated, and which security practices are actually tested. This page is readiness guidance, not legal advice or a compliance certification.</p>
      </section>

      <section>
        <h2>What is established, and what it means for suppliers</h2>
        <table>
          <thead><tr><th>Source-backed fact</th><th>Practical supplier implication</th></tr></thead>
          <tbody>
            <tr><td>The European Commission states that NIS2 creates a unified cybersecurity framework across 18 critical sectors. As a rule, medium-sized and large covered entities must take appropriate cybersecurity risk-management measures and notify significant incidents.</td><td>If a client is in a covered sector, its supplier questionnaires may become more specific about access control, backup, incident handling and supply-chain security.</td></tr>
            <tr><td>The Commission also highlights top-management accountability for non-compliance with cybersecurity risk-management measures.</td><td>Client security requests are no longer only technical requests; they may be procurement, legal and management-risk requests.</td></tr>
            <tr><td>European DIGITAL SME says small and micro enterprises are generally exempt from direct NIS2 obligations, but supply-chain security can make SMEs face higher cybersecurity expectations from clients.</td><td>A supplier can be outside direct NIS2 scope and still need to prove credible cybersecurity practices to win or keep contracts.</td></tr>
            <tr><td>DIGITAL SME reports that over 50% of surveyed SMEs are unclear about NIS2 requirements, especially how to prove trustworthiness within the supply chain.</td><td>A simple, evidence-based readiness file is commercially useful even before a formal certification project.</td></tr>
            <tr><td>ENISA’s NIS2 technical implementation guidance provides practical advice, examples of evidence and mappings, but states that the guidance is advisory and not a legal compliance guarantee.</td><td>Use ENISA as a quality reference for evidence thinking, but check national rules and client-specific contractual clauses before making legal claims.</td></tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>Readiness checklist before answering a client questionnaire</h2>
        <h3>1. Scope and client context</h3>
        <ul>
          <li>Identify which client, service, data flow and contract the questionnaire concerns.</li>
          <li>State whether your answer covers the whole company, one business unit, one SaaS service, or one project.</li>
          <li>Do not claim direct NIS2 applicability or exemption unless legal counsel or a competent authority has confirmed it.</li>
        </ul>

        <h3>2. Assets, accounts and data</h3>
        <ul>
          <li>List the systems used to deliver the service: email, identity provider, endpoints, cloud storage, finance tools, production systems and key SaaS platforms.</li>
          <li>Classify client data at a practical level: no client data, business contact data, confidential documents, credentials, production access, or regulated data.</li>
          <li>Assign an owner for each critical system and keep the list updated after major tool changes.</li>
        </ul>

        <h3>3. Access control and MFA</h3>
        <ul>
          <li>Enforce multi-factor authentication for email, identity, backup, finance, code, remote access and administrator accounts.</li>
          <li>Use individual named accounts rather than shared admin accounts wherever possible.</li>
          <li>Record who can approve access for new staff, contractors and emergency recovery.</li>
        </ul>

        <h3>4. Backup, continuity and recovery</h3>
        <ul>
          <li>Define recovery time objective (RTO) and recovery point objective (RPO) for the systems that affect client delivery.</li>
          <li>Keep at least one backup path that is offline, immutable or strongly access-controlled.</li>
          <li>Run and document restore tests. A screenshot of “backup successful” is weaker than a dated restore-test note.</li>
        </ul>

        <h3>5. Incident handling and escalation</h3>
        <ul>
          <li>Name the person who can declare a security incident, contact external support and notify affected clients under contract.</li>
          <li>Write a short escalation path for suspected ransomware, email compromise, lost device, credential exposure and data leak.</li>
          <li>Keep emergency contacts outside the systems that might be locked during an incident.</li>
        </ul>

        <h3>6. Vulnerability and patch management</h3>
        <ul>
          <li>Document how operating systems, browsers, productivity tools, servers, plugins and exposed services are updated.</li>
          <li>Prioritise internet-facing systems and tools that store client data.</li>
          <li>If you cannot patch quickly, document compensating controls or the decision owner.</li>
        </ul>

        <h3>7. Your own suppliers and subcontractors</h3>
        <ul>
          <li>List critical third parties used to deliver the client service: hosting, SaaS, MSP, accounting, ticketing, development or file-sharing platforms.</li>
          <li>Keep public security, privacy or compliance pages for those vendors where available.</li>
          <li>Make clear which controls are yours and which depend on a vendor contract or platform feature.</li>
        </ul>

        <h3>8. Evidence pack</h3>
        <ul>
          <li>Prepare a concise document set before the client asks: access-control summary, backup summary, incident-escalation summary, supplier list and last restore-test record.</li>
          <li>Redact secrets, customer names, internal IP addresses and personal staff details before sharing evidence.</li>
          <li>Keep version dates. A two-page current summary is better than a large, stale policy folder.</li>
        </ul>
      </section>

      <section>
        <h2>Evidence matrix for SME suppliers</h2>
        <table>
          <thead><tr><th>Client question</th><th>Stronger answer</th><th>Evidence to prepare</th><th>Do not share</th></tr></thead>
          <tbody>
            <tr><td>Do you use MFA?</td><td>MFA is enforced for administrator, email, identity and backup accounts.</td><td>Short policy excerpt, admin setting screenshot with sensitive names redacted, exception register if any.</td><td>Recovery codes, staff phone numbers, full user list.</td></tr>
            <tr><td>Can you recover from ransomware?</td><td>Critical systems have defined RTO/RPO targets and restore tests are documented.</td><td>Backup architecture summary, last restore-test date, owner and result.</td><td>Backup credentials, exact network paths, unredacted incident reports.</td></tr>
            <tr><td>How do you handle incidents?</td><td>Named owner, escalation path and client-notification handoff are documented.</td><td>One-page incident escalation summary and emergency contact roles.</td><td>Personal mobile numbers unless contractually required and consented.</td></tr>
            <tr><td>How do you manage suppliers?</td><td>Critical third parties are listed and reviewed when contracts or services change.</td><td>Supplier register with service purpose, data category and public security references.</td><td>Commercially sensitive contracts unless reviewed.</td></tr>
            <tr><td>Do you have security policies?</td><td>Policies exist for access, backup, incident escalation, acceptable use and supplier review, scaled to company size.</td><td>Versioned policy summaries, approval date, owner, review cadence.</td><td>Copied generic templates that do not match actual practice.</td></tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>Software buying implications</h2>
        <p>This page does not rank vendors. It defines what an SME should be able to prove before comparing products.</p>
        <ul>
          <li>If MFA and shared-account control are weak, evaluate a business password manager or identity/access-management improvement before buying more dashboards.</li>
          <li>If restore testing is missing, prioritise backup or DRaaS products that make restore workflows, immutable retention and test evidence easy to document.</li>
          <li>If the questionnaire asks for monitoring, logging or response capacity that the company cannot operate internally, consider a qualified MSP or MSSP rather than unmanaged tools.</li>
          <li>If policies are missing, fix the operating procedure first. A compliance-looking PDF that nobody follows is weaker than a short documented process that is tested.</li>
        </ul>
      </section>

      <section>
        <h2>Fast readiness score</h2>
        <p>Score each line from 0 to 2. Below 10/20, fix the basics before sending confident supplier-security answers. Between 10 and 15, build evidence and close gaps. At 16 or above, prepare client-specific responses and legal review for contractual claims.</p>
        <table>
          <thead><tr><th>Control</th><th>0</th><th>1</th><th>2</th></tr></thead>
          <tbody>
            <tr><td>Scope of questionnaire</td><td>Unknown</td><td>Informal</td><td>Written and bounded</td></tr>
            <tr><td>Asset and SaaS inventory</td><td>None</td><td>Partial</td><td>Critical systems listed with owners</td></tr>
            <tr><td>MFA coverage</td><td>No</td><td>Some key accounts</td><td>All admin, email, identity and backup accounts</td></tr>
            <tr><td>Shared admin accounts</td><td>Common</td><td>Exceptions exist</td><td>Named accounts by default</td></tr>
            <tr><td>RTO/RPO</td><td>Not defined</td><td>One critical system only</td><td>Defined for client-impacting systems</td></tr>
            <tr><td>Backup protection</td><td>Reachable by normal admin account</td><td>Some separation</td><td>Offline, immutable or strongly access-controlled copy</td></tr>
            <tr><td>Restore-test evidence</td><td>Never tested</td><td>Old or informal test</td><td>Dated test record with result</td></tr>
            <tr><td>Incident owner</td><td>No owner</td><td>One informal owner</td><td>Named owner plus backup owner</td></tr>
            <tr><td>Patch process</td><td>Ad hoc</td><td>Partly documented</td><td>Documented for exposed and critical systems</td></tr>
            <tr><td>Supplier register</td><td>None</td><td>Partial vendor list</td><td>Critical suppliers mapped to service and data category</td></tr>
          </tbody>
        </table>
      </section>

      <section class="cta-panel">
        <h2>Next step</h2>
        <p>If ransomware recovery is the weakest part of the evidence pack, start with the recovery checklist before comparing backup vendors.</p>
        <a class="button primary" href="/en/ransomware-recovery-checklist-small-business/">Use the ransomware recovery checklist</a>
      </section>

      <section>
        <h2>Sources and limits</h2>
        <ul>
          <li>European Commission, NIS2 Directive: securing network and information systems. <a href="https://digital-strategy.ec.europa.eu/en/policies/nis2-directive">https://digital-strategy.ec.europa.eu/en/policies/nis2-directive</a></li>
          <li>ENISA, NIS2 Technical Implementation Guidance. The guidance includes practical advice, examples of evidence and mappings, but is advisory and not a legal compliance guarantee. <a href="https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance">https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance</a></li>
          <li>European DIGITAL SME Alliance, guide to position SMEs as trusted NIS2 suppliers. <a href="https://www.digitalsme.eu/digital-sme-launches-guide-to-position-smes-as-trusted-nis2-suppliers/">https://www.digitalsme.eu/digital-sme-launches-guide-to-position-smes-as-trusted-nis2-suppliers/</a></li>
        </ul>
        <p><strong>Disclaimer:</strong> this is educational supplier-readiness material for SMEs. It is not legal advice, not a NIS2 applicability assessment, not a certification, and not a substitute for national competent-authority guidance or qualified counsel.</p>
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
    rto_rpo_calculator = Page(
        "en",
        CORE_SLUGS["rto_rpo_calculator"]["en"],
        "RTO/RPO calculator for small business",
        "A browser-only RTO/RPO calculator for small businesses defining backup, restore and ransomware recovery requirements before vendor comparison.",
        rto_rpo_calculator_body(),
        commercial=True,
    )
    pages_by_key["rto_rpo_calculator"]["en"] = rto_rpo_calculator
    pages.append(rto_rpo_calculator)
    nis2_supplier_readiness = Page(
        "en",
        CORE_SLUGS["nis2_supplier_readiness"]["en"],
        "NIS2 supplier cybersecurity readiness checklist for SMEs",
        "A source-backed, non-legal NIS2 supplier cybersecurity readiness checklist for SME suppliers preparing client questionnaires and evidence packs.",
        nis2_supplier_readiness_body(),
        commercial=True,
    )
    pages_by_key["nis2_supplier_readiness"]["en"] = nis2_supplier_readiness
    pages.append(nis2_supplier_readiness)
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
select, input { padding:11px 12px; border:1px solid var(--line); border-radius:12px; background:white; font:inherit; }
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

(function () {
  const form = document.getElementById('rto-rpo-calculator');
  const output = document.getElementById('rto-rpo-output');
  if (!form || !output) return;

  const processLabels = {
    email: 'Email and calendar',
    finance: 'Accounting, billing or payroll',
    client_files: 'Client files or project delivery',
    production: 'Production, booking or revenue system',
    identity: 'Identity, admin or password vault'
  };

  const formatHours = function (hours) {
    if (hours === 0) return 'near-zero data loss';
    if (hours < 1) return Math.round(hours * 60) + ' minutes';
    if (hours === 1) return '1 hour';
    if (hours % 24 === 0) {
      const days = hours / 24;
      return days === 1 ? '1 day' : days + ' days';
    }
    return hours + ' hours';
  };

  const safeNumber = function (formData, key) {
    const value = Number.parseFloat(formData.get(key));
    return Number.isFinite(value) && value >= 0 ? value : 0;
  };

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    const process = processLabels[data.get('process')] || 'Selected process';
    const downtime = Math.max(0.25, safeNumber(data, 'downtime'));
    const dataLoss = safeNumber(data, 'data_loss');
    const people = safeNumber(data, 'people');
    const hourlyCost = safeNumber(data, 'hourly_cost');
    const workaround = data.get('workaround');
    const exposure = downtime * people * hourlyCost;

    let tier = 'Flexible recovery tier';
    let implication = 'A slower, lower-cost backup pattern may be acceptable only if this process is genuinely non-critical and the workaround has been tested.';
    const requirements = [
      'Document the system owner, restore owner and escalation owner.',
      'Run a restore test and keep the date, duration, result and next fix.',
      'Protect backup and administrator accounts with MFA.'
    ];

    if (downtime <= 4 || dataLoss <= 1) {
      tier = 'Critical recovery tier';
      implication = 'The target is tight. Treat this as a managed recovery requirement, not a casual file-backup requirement.';
      requirements.push('Ask vendors for frequent recovery points, immutable or strongly protected retention, tested restore workflows and support response terms.');
    } else if (downtime <= 24 || dataLoss <= 24) {
      tier = 'Standard business-critical tier';
      implication = 'Daily or more frequent automated backup may fit, but only if restore testing proves the target is realistic.';
      requirements.push('Ask vendors for SaaS coverage, clear restore steps, retention policy, admin audit logs and documented recovery testing.');
    } else {
      requirements.push('Write down why slower recovery is acceptable and which workarounds keep the business operating.');
    }

    if (workaround === 'none' && downtime > 24) {
      requirements.push('Because no reliable workaround exists, reconsider whether the RTO can safely exceed 24 hours.');
    }
    if (dataLoss === 0) {
      requirements.push('Near-zero data loss usually requires specialised architecture. Validate feasibility before promising it to clients.');
    }

    const exposureText = exposure > 0
      ? exposure.toLocaleString(undefined, { maximumFractionDigits: 0 }) + ' currency units at the selected RTO'
      : 'not estimated because people or hourly cost is zero';

    output.hidden = false;
    output.innerHTML = '<h2>' + tier + '</h2>' +
      '<p><strong>Process:</strong> ' + process + '</p>' +
      '<ul>' +
      '<li><strong>Suggested RTO:</strong> restore within ' + formatHours(downtime) + ' or faster.</li>' +
      '<li><strong>Suggested RPO:</strong> recover to a point no older than ' + formatHours(dataLoss) + '.</li>' +
      '<li><strong>Approximate staff downtime exposure:</strong> ' + exposureText + '.</li>' +
      '</ul>' +
      '<p><strong>Interpretation:</strong> ' + implication + '</p>' +
      '<h3>Minimum requirements to document</h3><ol>' + requirements.map(item => '<li>' + item + '</li>').join('') + '</ol>' +
      '<p class="microcopy">This is a rough planning estimate. It does not prove that any vendor or internal process can meet the target until a restore test has been completed.</p>';
  });
})();
"""


if __name__ == "__main__":
    target = Path(os.getenv("SITE_OUTPUT", "dist"))
    build_site(target)
    print(f"Built {SITE_NAME} into {target.resolve()}")
