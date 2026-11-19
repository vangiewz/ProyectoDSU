# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS with plain JavaScript, no framework or build step (confirmed 18/11/2026). Deployed on Vercel.

## Users

Institutional buyers: heads of general/university services, municipal sanitation units and facility managers of companies with large campuses in Bolivia, evaluating whether to contract a waste-collection management platform. Secondary audiences: current client staff looking for support and release notes, and investors reviewing the company.

## Product Purpose

Corporate site of Residata S.R.L., a Bolivian software company. It presents Residata, a SaaS platform for solid-waste collection management with generation forecasting (Random Forest Regressor), explains plans and prices, publishes product updates, and gives support and contact channels. Success: a qualified institution requests a demo or contacts the company; existing clients resolve doubts without calling.

## Positioning

Residata works with the scales and phones a collection crew already has, without importing fill-level sensors or proprietary bins (unlike Sensoneo, Ecube Labs or Bigbelly). Every emptying is weighed in kilograms, and forecasts are trained on the institution's own calendar (classes, exams, breaks).

## Operating Context

The product was built and piloted for the Dirección de Servicios Universitarios (DSU) of the UAGRM in Santa Cruz de la Sierra: field operators register weighings from a phone, supervisors plan routes and crews, directors read dashboards, heat maps and forecasts, and an administrator manages users, catalogs, ETL and the model.

## Capabilities and Constraints

Confirmed platform capabilities: field registration from mobile, route/crew/vehicle planning, incidents, KPI dashboard and Power BI model, campus heat map, Random Forest forecast with alerts and logistic recommendations, Excel/PDF reports, audit log, four roles. Production: API on Azure VM (Mexico Central, Docker + Caddy), PostgreSQL on Neon, web on Vercel. Contact email: rekteado@gmail.com. No phone/WhatsApp number published.

Plan prices come from the market study (DocumentoSoftware2/finanzas.py, 18/11/2026): Inicial Bs 0, Campus Bs 2 900/month, Red Bs 7 500/month (annual = 10 months), implementation Bs 9 000 / Bs 18 000. Service terms confirmed by the user (18/11/2026): monthly availability commitment 99 % (Campus) and 99,5 % (Red) with a 10 % fee credit per missing point; first support response 8 business hours (Campus) and 4 (Red); contact replies within one business day.

## Brand Commitments

Company name Residata S.R.L.; product name Residata. Founders: Carlos Gabriel Lobo Gutiérrez and Leonardo Serrate Basma. Language: Spanish (Bolivia), formal "usted"-free neutral tone.

## Evidence on Hand

Real screenshots of the DSU system in `../docs/auditoria-fase-final/ui/`. Single pilot client (DSU-UAGRM); no other customers, testimonials or press exist and must not be invented. Forecast accuracy on institutional data is not yet validated; do not publish accuracy claims.

## Product Principles

- Truth over hype: only claims backed by the running system.
- Local fit: Bolivian prices in Bs, Bolivian law, hardware already on hand.
- Every visitor leaves with a next step: demo, plan, ticket or release note.
