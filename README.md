# ct-ee-domain-pulling
Quick and dirty codebase to fetch and save .ee domains from the most popular certificate log lists as of 2025

# A few interesting notes
While running the `*-cert-collection.py` scripts, I noticed a ton of "hostname mismatch" errors. At first, I was happy that the Python SSL library handles such cases. However, after taking a closer look, I'm weirded out.

Some examples of error-throwing websites include `tartuseikluspark.ee` (Tartu Adventure Park), `skenergia.ee` (Narva Sports School "Energia") and `npsk.ee` (Narva Paemurru Sports School). 
Due to the mismatched certificate, my HTTPS-only browser throws a ton of errors my way. `tartuseikluspark.ee` opts for a non-secure HTTP connection for the website while `npsk.ee` redirects to `uus.npsk.ee`, which is fine.

Checking the CN entries reveals the following: the domain `npsk.ee` has the certificate for `*.tll07.zoneas.eu` (Zone is a major Estonian hosting provider) and so does `tartuseikluspark.ee`. `skenergia.ee` has the CN `h5.compic.ee`.

...why?

Full list of examples will be in a separate file. For now, I'll store them here:
```text
tartuseikluspark.ee
skenergia.ee
npsk.ee
epls.ee
psyhhoanalyys.ee
suhtlemisoskused.ee
hyva.ee
gestalt.ee
laurlaur.ee
taherootsmae.ee
reflektoorium.ee
perenouandla.ee
synergia.ee
tervisekunstid.ee
helenalass.ee
els.ee
esks.ee
unemeditsiin.ee
esves.ee
lounaeestivahiuhing.org
tromboos.ee
kaev.ee
naudikauem.ee
kuivaks.ee
mortematus.ee
arcokivi.ee
johvikivi.ee
lovatalu.ee
ginger.ee
teraapiakeskus.ee
kyyned.ee
liilia.net

```

Also handshake failures from
```text
ulitundlikinimene.ee
insait.ee

```

EE cert key too weak:
```text
ohatis.ee

```
