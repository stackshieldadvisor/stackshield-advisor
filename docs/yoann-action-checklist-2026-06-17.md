# StackShield Advisor — Checklist exacte pour Yoann

**Objectif :** rendre Hemera autonome le plus vite possible sur publication, mesure, contenu et préparation de monétisation, tout en gardant Yoann anonyme publiquement.

---

## 0. Règle centrale

L'anonymat signifie :

- le public ne voit pas Yoann ;
- le site ne mentionne pas Yoann, INSERM, la thèse ou le labo ;
- les comptes publics utilisent une marque séparée.

Mais l'anonymat ne signifie pas :

- cacher son identité aux banques ;
- cacher son identité aux plateformes d'affiliation ;
- éviter les obligations fiscales ;
- utiliser de fausses informations KYC.

Les plateformes de paiement et d'affiliation peuvent demander identité réelle, adresse, pays fiscal, documents ou formulaires fiscaux. Yoann doit remplir ces informations lui-même. Hemera ne doit jamais recevoir de pièce d'identité, mot de passe bancaire ou accès bancaire.

---

## 1. Priorité absolue : mettre le site en ligne gratuitement

Sans site public, pas d'indexation, pas d'affiliation sérieuse, pas de mesure.

### Option recommandée

**GitHub anonyme + Cloudflare Pages gratuit**

Pourquoi :

- gratuit ;
- déploiement automatique ;
- bon pour site statique ;
- possibilité de garder une marque séparée ;
- je peux mettre à jour le site si j'ai accès au dépôt GitHub ;
- pas besoin d'acheter un domaine.

### Action Yoann A — créer une adresse email séparée

Créer une adresse dédiée, par exemple :

```text
stackshieldadvisor@gmail.com
stackshieldadvisor@proton.me
stackshield.ops@gmail.com
```

Ne pas utiliser :

```text
yoann.fraysse@inserm.fr
yofraysse@gmail.com
```

### Action Yoann B — créer un compte GitHub anonyme

URL : https://github.com/signup

Paramètres recommandés :

- Username : `stackshield-advisor`, `stackshield-labs`, `securestack-advisor` ou équivalent disponible.
- Email : adresse dédiée créée en A.
- Ne pas ajouter photo personnelle.
- Ne pas ajouter nom complet.
- Ne pas lier à ton GitHub personnel.

Créer ensuite un dépôt :

URL : https://github.com/new

Réglages :

```text
Repository name: stackshield-advisor
Visibility: Public
Add README: No
Add .gitignore: No
Choose a license: No
```

Pourquoi public : GitHub Pages public gratuit et Cloudflare peut lire facilement le repo. Si tu veux privé, Cloudflare Pages peut fonctionner, mais ça ajoute de la complexité.

### Action Yoann C — créer un token GitHub limité

URL : https://github.com/settings/personal-access-tokens/new

Choisir : **Fine-grained token**.

Réglages :

```text
Token name: hemera-stackshield-deploy
Expiration: 90 days
Repository access: Only select repositories
Selected repository: stackshield-advisor
Permissions:
- Contents: Read and write
- Workflows: Read and write uniquement si on choisit GitHub Pages avec Actions
```

Si Cloudflare Pages est utilisé, `Contents: Read and write` suffit généralement pour que je pousse les fichiers. Si GitHub Pages avec Actions est choisi, il faudra aussi `Workflows: Read and write`.

Ne colle pas le token dans le chat.

Dépose-le ici :

```text
/icloud/Dépot Hemera/stackshield_access/github_token.txt
```

Créer aussi :

```text
/icloud/Dépot Hemera/stackshield_access/repo_url.txt
```

Avec dedans l'URL du dépôt, par exemple :

```text
https://github.com/stackshield-advisor/stackshield-advisor.git
```

### Action Yoann D — créer un compte Cloudflare

URL : https://dash.cloudflare.com/sign-up

Utiliser la même adresse dédiée.

Puis :

1. Aller dans le dashboard Cloudflare.
2. Menu gauche : **Workers & Pages**.
3. Cliquer **Create application**.
4. Onglet **Pages**.
5. Choisir **Connect to Git**.
6. Connecter le compte GitHub anonyme.
7. Sélectionner le repo `stackshield-advisor`.
8. Paramètres build :

```text
Framework preset: None
Build command: python3 src/generate_site.py
Build output directory: dist
Root directory: /
```

Si Cloudflare demande la branche :

```text
main
```

Résultat attendu :

```text
https://stackshield-advisor.pages.dev
```

ou un nom proche.

Déposer l'URL finale dans :

```text
/icloud/Dépot Hemera/stackshield_access/public_url.txt
```

---

## 2. Mesure SEO : Google Search Console

À faire après publication.

URL : https://search.google.com/search-console

Action :

1. Cliquer **Add property**.
2. Choisir **URL prefix**.
3. Mettre l'URL Cloudflare Pages, par exemple :

```text
https://stackshield-advisor.pages.dev/
```

4. Choisir une méthode de vérification.

Méthode recommandée : **HTML tag** ou **HTML file**.

Si Google donne un fichier HTML :

Dépose-le ici :

```text
/icloud/Dépot Hemera/stackshield_access/google_search_console_verification.html
```

Si Google donne une balise meta :

Dépose-la ici :

```text
/icloud/Dépot Hemera/stackshield_access/google_search_console_meta.txt
```

Je l'intégrerai au site.

Ensuite, soumettre le sitemap :

```text
https://stackshield-advisor.pages.dev/sitemap.xml
```

---

## 3. Monétisation : comptes à créer mais sans précipitation

### 3.1 Plateformes prioritaires

Créer ces comptes uniquement après que le site soit public, ou au moins prêt à l'être.

#### PartnerStack

URL : https://partnerstack.com/partners-and-publishers  
Marketplace : https://market.partnerstack.com/

Pourquoi : B2B SaaS, Keeper business, nombreux programmes SaaS.

#### CJ Affiliate

URL directe publisher : https://signup.cj.com/member/signup/publisher/  
Page générale : https://www.cj.com/join

Pourquoi : Acronis utilise Commission Junction / CJ pour son programme affilié.

#### Impact

URL : https://impact.com/partners/affiliate-partners/

Pourquoi : beaucoup de programmes logiciels/SaaS, utile plus tard.

### 3.2 Programmes à viser en premier

Ne pas candidater partout d'un coup. Ordre recommandé :

1. Acronis — backup / cyber protection.
2. Keeper Security — business password manager / CPL leads.
3. NordPass — B2B password manager.
4. Perimeter 81 / Check Point SASE — plus tard, après pages SASE/VPN.

### 3.3 Informations que Yoann devra remplir lui-même

Ces plateformes peuvent demander :

- nom légal ;
- pays ;
- adresse ;
- email ;
- site web ;
- méthode de paiement ;
- statut fiscal ;
- formulaire fiscal ;
- parfois PayPal, Stripe ou compte bancaire.

Ne jamais me donner :

- mot de passe bancaire ;
- accès banque ;
- pièce d'identité ;
- numéro complet de carte ;
- informations fiscales sensibles dans le chat.

Ce que tu peux me donner :

- confirmation que le compte est créé ;
- nom des programmes acceptés/refusés ;
- lien affilié final ;
- conditions de commission copiées sans données personnelles.

---

## 4. Argent et statut administratif

Un compte bancaire seul ne suffit pas à monétiser.

Il peut servir à recevoir l'argent, mais il faut une plateforme qui collecte ou attribue les revenus :

- PartnerStack ;
- CJ ;
- Impact ;
- Stripe ;
- PayPal ;
- Wise ;
- autre.

Avant d'encaisser régulièrement : vérifier la compatibilité avec ton statut professionnel et fiscal.

Point sensible : Yoann est en CDD INSERM. Il faut vérifier si une activité commerciale accessoire est autorisée ou nécessite une déclaration/autorisation. Hemera ne doit pas donner de conseil juridique définitif. Si nécessaire, Hemera peut préparer un mail discret et neutre pour demander les règles générales d'activité accessoire sans mentionner le projet en détail.

Décision recommandée :

- Construire et publier gratuitement maintenant.
- Candidater aux programmes affiliés ensuite.
- Ne pas encaisser de revenus importants sans clarification fiscale/statutaire.

---

## 5. Budget

Budget recommandé maintenant :

```text
0 €/mois
```

Aucun domaine au départ.

Domaine à envisager seulement si :

- un programme affilié refuse le sous-domaine gratuit ;
- Search Console montre des impressions/clics ;
- le site commence à recevoir des backlinks ;
- on veut améliorer la crédibilité.

Budget domaine possible plus tard :

```text
10–20 €/an
```

Mais pas maintenant.

---

## 6. Ce que Yoann doit me fournir maintenant

Checklist minimale pour rendre Hemera autonome :

```text
[ ] Adresse email dédiée créée
[ ] Compte GitHub anonyme créé
[ ] Repo GitHub public stackshield-advisor créé
[ ] Token GitHub limité créé
[ ] github_token.txt déposé dans /icloud/Dépot Hemera/stackshield_access/
[ ] repo_url.txt déposé dans /icloud/Dépot Hemera/stackshield_access/
[ ] Compte Cloudflare créé
[ ] Cloudflare Pages connecté au repo GitHub
[ ] public_url.txt déposé dans /icloud/Dépot Hemera/stackshield_access/
[ ] Google Search Console lancé après publication
[ ] Fichier ou meta tag de vérification Search Console déposé si nécessaire
```

Phrase à envoyer à Hemera quand c'est fait :

```text
J'ai créé l'accès StackShield. Les fichiers sont dans /icloud/Dépot Hemera/stackshield_access/.
```

---

## 7. Ce que Hemera fera ensuite

Dès que les accès sont prêts :

1. Copier le projet local dans le repo GitHub.
2. Ajouter si nécessaire la configuration de build.
3. Pousser le site.
4. Vérifier le déploiement public.
5. Ajouter Search Console verification si fournie.
6. Soumettre ou préparer le sitemap.
7. Continuer la boucle quotidienne.
8. Préparer les candidatures affiliées, mais ne pas les soumettre sans validation humaine.

---

## 8. Priorité unique pour Yoann

Si tu ne fais qu'une chose :

# Crée l'adresse dédiée + le GitHub anonyme + le repo + le token limité.

Sans ça, Hemera peut produire localement, mais ne peut pas rendre le site vivant et mesurable.

Avec ça, Hemera peut devenir réellement autonome sur la construction, le déploiement et l'amélioration quotidienne.
