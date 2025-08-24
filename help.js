
export function mountHelp(buttonTarget=document.body){
  const backdrop = document.createElement('div'); backdrop.className='modal-backdrop'; backdrop.id='helpBackdrop';
  const modal = document.createElement('div'); modal.className='modal';
  modal.innerHTML = `
    <header>
      <h3>Fiche mémo — Lecture du tableau financier</h3>
      <button id="helpClose" class="btn btn-neutral">Fermer</button>
    </header>
    <div class="hr"></div>
    <section>
      <h4>🔤 Vocabulaires clés</h4>
      <ul style="line-height:1.6">
        <li><strong>BAC</strong> : budget total prévu.</li>
        <li><strong>AC</strong> : dépenses à date.</li>
        <li><strong>EV</strong> : valeur produite = BAC × avancement.</li>
        <li><strong>CPI</strong> = EV/AC : perf. coût (1=OK, <1 surcoût).</li>
        <li><strong>SPI</strong> = EV/PV : perf. délai (proxy).</li>
        <li><strong>EAC</strong> = AC + ETC : coût projeté final.</li>
      </ul>
    </section>
    <section>
      <h4>🎯 Règles simples</h4>
      <ul style="line-height:1.6">
        <li><span class="badge ok">CPI ≥ 1.00</span> • <span class="badge wa">0.95–1.00</span> • <span class="badge cr">< 0.95</span></li>
        <li>% Budget utilisé : vert < 50%, orange 80–95%, rouge >95%.</li>
        <li>Marge = Devis – EAC (si <0 ⇒ alerte rouge).</li>
      </ul>
    </section>
    <section>
      <h4>📊 Lire les graphiques</h4>
      <ul style="line-height:1.6">
        <li>Barres : Budgété vs Dépensé par catégorie.</li>
        <li>Donut : AC/BAC = part du budget consommé.</li>
        <li>Burn-up : points EV (orange) et AC (rouge) vs ligne BAC (gris).</li>
      </ul>
    </section>
    <section>
      <h4>🧠 Bonnes pratiques</h4>
      <ul style="line-height:1.6">
        <li>Préciser l’avancement par catégorie quand possible (EAC plus fiable).</li>
        <li>Adapter les seuils d’alerte au chantier (ex : 75% / 90%).</li>
        <li>Noter les décisions → journal de bord.</li>
      </ul>
    </section>
  `;
  backdrop.appendChild(modal);
  document.body.appendChild(backdrop);

  function open(){ backdrop.style.display='flex'; }
  function close(){ backdrop.style.display='none'; }
  modal.querySelector('#helpClose').addEventListener('click', close);
  backdrop.addEventListener('click', (e)=>{ if(e.target===backdrop) close(); });

  const btn = document.createElement('button');
  btn.className='btn btn-neutral help-button'; btn.id='helpOpen';
  btn.textContent = 'ℹ️ Info';
  btn.addEventListener('click', open);
  buttonTarget.appendChild(btn);

  window.addEventListener('keydown', (e)=>{ if(e.key==='?' && !e.ctrlKey && !e.metaKey){ open(); } });
}
