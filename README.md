# StackShield Advisor

Anonymous static lead-generation prototype for small-business cybersecurity and backup software guidance.

## Current state

- Static generator: `src/generate_site.py`
- Tests: `tests/test_site_generator.py`
- Built site: `dist/`
- Public site: https://stackshieldadvisor.github.io/stackshield-advisor/
- Source repository: https://github.com/stackshieldadvisor/stackshield-advisor
- Deployment script: `scripts/deploy_github_pages.py`
- Market research: `docs/market-research-2026-06-17.md`
- Yoann action checklist: `docs/yoann-action-checklist-2026-06-17.md`
- Languages: English, French, Spanish, German
- No paid domain required for validation
- No email collection in the prototype recommender
- Affiliate disclosure and privacy/methodology pages included

## Build

```bash
python3 -m unittest discover tests -v
SITE_BASE_URL="https://stackshieldadvisor.github.io/stackshield-advisor" SITE_PATH_PREFIX="/stackshield-advisor" python3 src/generate_site.py
```

The site builds into `dist/`.

## Deploy

```bash
python3 scripts/deploy_github_pages.py
```

This command runs tests, builds the site for GitHub project Pages, commits source changes if needed, pushes `main`, and publishes `dist/` to the `gh-pages` branch.

## Free deployment options

### Recommended first choice: Cloudflare Pages

Free subdomain format:

```text
https://stackshield-advisor.pages.dev
```

Pros:

- free static hosting;
- strong speed/security;
- no paid domain required;
- easy later domain connection;
- good for anonymous brand validation.

### Other free options

- GitHub Pages: `https://<username>.github.io/<repo>/`
- Netlify: `https://<project>.netlify.app`
- Vercel: `https://<project>.vercel.app`

## Do we need to buy a domain?

No, not for the validation phase.

A custom domain is useful later for trust, branding, email deliverability and resale value. But the first objective is to validate indexing, impressions, clicks and conversion. Free hosting is enough for that.

Decision rule:

- Month 0–2: free subdomain.
- Buy a domain only if Search Console shows traction or if an affiliate program requires a professional domain.

## Can a bank account alone collect money?

Usually, no.

A normal bank account can receive payouts, but it is not itself a payment processor or affiliate account.

For monetization:

1. Affiliate programs may pay to a bank account, PayPal, Wise, Stripe or platform wallet depending on the program.
2. Direct product sales require a merchant/payment layer such as Stripe, Gumroad, Payhip, Lemon Squeezy, Paddle or equivalent.
3. Selling leads directly requires invoices, contracts and a compliant data-transfer process.

So the bank account is necessary but not sufficient. It is the payout destination, not the monetization infrastructure.

## Anonymity principle

Use a separate brand. Do not publish Yoann's name. Do not link to the PhD, lab, INSERM, or thesis work.

Recommended public identity:

```text
StackShield Advisor Editorial Team
```

## Language strategy

Initial languages:

1. English — largest commercial search surface and SaaS affiliate ecosystem.
2. French — useful for France/EU SMEs and Yoann can easily audit quality.
3. Spanish — large search surface, especially SMEs.
4. German — strong B2B/cyber/compliance market, but quality bar must be high.

Operational rule:

- English pages are source-of-truth.
- French can be high quality.
- Spanish/German should begin with fewer pages and be expanded only when page templates and claims are stable.

## Monetization path

Phase 1: affiliate only, no personal lead collection.

Phase 2: optional newsletter/lead magnet with explicit consent.

Phase 3: lead generation only after privacy policy, consent language, retention rules and partner-transfer terms are ready.

## Quality rule

Do not publish pages that lack at least three of these:

- decision matrix;
- checklist;
- source-backed claims;
- specific business segment;
- calculator/tool;
- conditional recommendation.

## Current validation commands already passed

```text
python3 -m unittest tests/test_site_generator.py -v
# Ran 5 tests — OK

python3 src/generate_site.py
# Built StackShield Advisor into /root/projects/stackshield-advisor/dist
# 29 generated files
```
