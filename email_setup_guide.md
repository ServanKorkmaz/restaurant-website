# E-post oppsett for Nawarat Thai Mat og Catering

## Slik setter restauranteieren opp e-post for kontaktskjemaet:

### Alternativ 1: Gmail SMTP (Anbefalt - Gratis)

1. **Opprett eller bruk eksisterende Gmail-konto**
   - Kan være nawarat.thai.mat@gmail.com eller annen Gmail-adresse

2. **Aktiver 2-trinns verifisering**
   - Gå til Gmail → Profil → "Manage your Google Account"
   - Security → 2-Step Verification → Slå på

3. **Generer app-passord**
   - I samme Security-meny → App passwords
   - Velg "Mail" → Generer passord
   - Kopier det 16-tegns passordet

4. **Legg til i Replit**
   - I Replit-prosjektet → Secrets (på venstre side)
   - Legg til:
     - `GMAIL_USER`: Gmail-adressen (f.eks. nawarat.thai.mat@gmail.com)
     - `GMAIL_APP_PASSWORD`: Det 16-tegns passordet fra Gmail

### Alternativ 2: SendGrid (Gratis opp til 100 e-poster/dag)

1. **Opprett SendGrid-konto**
   - Gå til https://sendgrid.com → Sign up
   - Velg gratis plan (100 e-poster/dag)

2. **Få API-nøkkel**
   - SendGrid dashboard → Settings → API Keys
   - Create API Key → Full Access → Kopier nøkkelen

3. **Legg til i Replit**
   - I Replit-prosjektet → Secrets
   - Legg til: `SENDGRID_API_KEY`: API-nøkkelen fra SendGrid

## Hvordan det fungerer:

- **Med oppsett**: E-post sendes direkte til post@nawaratthaimat.no
- **Uten oppsett**: Meldinger lagres i `contact_messages.log` som kan sjekkes i admin-panelet
- Kunder får alltid bekreftelse på at meldingen er mottatt

## Admin-panel tilgang:

Restauranteieren kan sjekke alle kontaktmeldinger via:
- Admin-panel: `/admin/login` 
- Loggfil: `contact_messages.log`