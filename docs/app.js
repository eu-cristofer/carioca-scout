/* CariocaScout dashboard — pure JS, read-only, contract = deals.json.
   Pure helpers first (testable in the console), DOM wiring last. */

const CIDADES = {
  POA: "Porto Alegre", FLN: "Florianópolis",
  NYC: "Nova York", FLR: "Florença",
};

const brl = (v) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const dataBr = (iso) =>
  new Date(iso + "T12:00:00").toLocaleDateString("pt-BR", {
    weekday: "short", day: "2-digit", month: "short", year: "numeric",
  });

/* Normalize a price series into polyline points for a 100x28 viewBox.
   Pure function — try it in the console:
   sparklinePoints([400, 390, 300]) */
function sparklinePoints(series, w = 100, h = 28, pad = 2) {
  if (!series || series.length === 0) return "";
  if (series.length === 1) return `0,${h / 2} ${w},${h / 2}`;
  const min = Math.min(...series);
  const max = Math.max(...series);
  const span = max - min || 1;
  return series
    .map((v, i) => {
      const x = (i / (series.length - 1)) * w;
      const y = pad + (1 - (v - min) / span) * (h - 2 * pad);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

function renderCard(template, deal) {
  const node = template.content.cloneNode(true);
  node.querySelector(".aeroportos").textContent =
    `${deal.origin} → ${deal.dest}`;
  node.querySelector(".queda-badge").textContent = `−${deal.drop_pct}%`;
  node.querySelector(".destino").textContent =
    CIDADES[deal.dest] ?? deal.dest;
  node.querySelector(".feriado").textContent = deal.holiday;
  node.querySelector(".preco-atual").textContent = brl(deal.price_brl);
  node.querySelector(".preco-base").textContent = brl(deal.baseline_brl);
  node.querySelector(".sparkline polyline")
    .setAttribute("points", sparklinePoints(deal.trend));
  node.querySelector(".data-viagem").textContent =
    `Viagem: ${dataBr(deal.travel_date)}`;
  return node;
}

function renderMessage(deck, cls, text) {
  const p = document.createElement("p");
  p.className = cls;
  p.textContent = text;
  deck.replaceChildren(p);
}

async function main() {
  const deck = document.getElementById("deck");
  const template = document.getElementById("card-template");
  const stamp = document.getElementById("generated-at");

  try {
    const res = await fetch("deals.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const payload = await res.json();

    stamp.textContent =
      "Atualizado em " + new Date(payload.generated_at)
        .toLocaleString("pt-BR");
    stamp.hidden = false;

    if (!payload.deals || payload.deals.length === 0) {
      renderMessage(deck, "estado-vazio",
        "Nenhuma promoção hoje. O scout continua de olho — volte amanhã.");
      return;
    }
    deck.replaceChildren(
      ...payload.deals.map((d) => renderCard(template, d)));
  } catch (err) {
    renderMessage(deck, "estado-erro",
      "Não foi possível carregar as promoções agora. " +
      "Verifique a conexão e recarregue a página.");
    console.error("CariocaScout:", err);
  }
}

main();
