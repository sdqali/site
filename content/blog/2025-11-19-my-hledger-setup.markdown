---
title: "My HLedger Setup"
date: 2025-11-19T17:21:19-08:00
draft: true
tags:
- hledger
- nginx
- jwt
ghcommentid: 146
bbcommentid: 139
---
From 2014 to 2023, I kept track of my finances in one way or another. I started out with Intuit's Mint - it did a good job of aggregating accounts and presenting consolidated views. At some point, I became weary of Intuit having passwords to all my financial accounts and decided to keep track of everything in a Google Sheet, fronted by a Google Form to enter data. This worked okay, but we noticed that the Google Form interface made it hard to enter transactions, and slowly we stopped entering transactions the day it happened. This eventually led us to YNAB [^1], but it's opinionated hyperfocus on budgeting felt restrictive. By this time, financial companies had started imlementing OAuth etc., and platforms like Plaid had increased their converage, and in most cases aggregators like Mint no longer needed to store passwords for accounts. So, we went back to Mint.

At some point, Intuit acquired CreditKarma and slowly decided to strangle Mint, nudging (or dragging) their users to CreditKarma[^6] [^7]. With the degraded experience, we slowly stopped paying attention.

Recently, I learned about Plain Text Accounting [^2] and Ledger CLI [^3] from Paul Gross's writings about implementig  a Ledger primitive on top of PostgreSQL [^4]. This led me to HLedger, an implementation of Ledger CLI in Haskell. After poking around, I saw that it had a JSON API [^5]. This seemed like the perfect base to build something on.

I set up an hledger-web instance and built an iOS app. Along the way, I realized that HLedger does not expose all of it's functionality through the JSON API. Even though my Haskell is not great, I managed to implement these end points:

```Haskell
/marketprices                      MarketPricesR         GET  -- Get Prices of Commodities converted to default currency, from Price directices and inferred from Transactions
/accounts/#AccountName             AccountR              GET  -- Get details of an account, including balances. Removes the need to get all transactions and compute balances from frontend
/balancereport                     BalanceReportR        GET  -- Runs a balance report
/budgets                           BudgetsR              GET  -- Lists budgets
/budgetreport                      BudgetReportR         PUT  -- Runs a budget report for a given time period
```

I deployed the hledger-web instance on an EC2 instance; with a CloudFlare tunnel [^9], and CloudFlare Service Token verification [^8]. The iOS app would pass the token for every call and CloudFlare would verify it. The app was a delight to use and it did everything we needed to track transactions and our budget.

```plantuml
@startuml
skinparam BackGroundColor transparent
skinparam SequenceBoxBackgroundColor transparent
participant "iOS app" as app
box EC2 instance
participant "CF Tunnel" as cft
participant "hledger-web" as hlw
participant "FileSytem" as fs
end box
app -> cft : GET|PUT {ServiceToken}
cft -> hlw: GET|PUT
hlw -> fs: Read/Write Journal File
note right #transparent
transactions
directives
...
end note
@enduml
```

But then I ran in to the inevitable Apple tax - my app would "expire" every week unless I push a new build to my phone or pay Apple for a Developer License. I didn't like paying $99 per year to run an app I built on a phone I paid for. So, I decided to rewrite it for the last remaining non-rent seeking platform - the web.

I was initially tempted to build the frontend with React as I was familiar with it, but decided to use Svelte instead -- it was an opportunity to try something I hadn't done before.





[^1]: [You Need A Budget](https://www.ynab.com/)
[^2]: [Plain Text Accounting](https://plaintextaccounting.org/)
[^3]: [Ledger CLI](https://ledger-cli.org/doc/ledger3.html)
[^4]: [Ledger Implementation in PostgreSQL](https://www.pgrs.net/2025/03/24/pgledger-ledger-implementation-in-postgresql/).
[^5]: [hledger-web JSON API](https://hledger.org/1.50/hledger-web.html#json-api)
[^6]: [The Demise Of Intuit Mint And Personal Financial Management](https://www.forbes.com/sites/ronshevlin/2023/11/06/the-demise-of-intuit-mint-and-personal-financial-management/)
[^7]: [Intuit's Mint App Shutting Down...Replacement Recommendations?](https://www.bogleheads.org/forum/viewtopic.php?t=415838)
[^8]: [Service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
[^9]: [CloudFlare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
