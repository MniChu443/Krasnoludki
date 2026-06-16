let c = document.getElementById("projekt_canvas");
let ctx = c.getContext("2d");

let dane = [];
let wynikiAlgorytmy = {};
let mapa = {};
let slownikParowania = {};
let trasaKsiecia = [];

let tryb = "mapa";
let zoom = 1.0;
let kx = 0;
let ky = 0;
let klik = false;
let sx = 0;
let sy = 0;
let hvr = -1;

let sk = 60;
let im1 = new Image();
let im2 = new Image();
im1.src = "domek.png";
im2.src = "kopalnia.png";

let menu = document.createElement("div");
menu.style.position = "fixed";
menu.style.bottom = "20px";
menu.style.left = "50%";
menu.style.transform = "translateX(-50%)";
menu.style.display = "flex";
menu.style.gap = "10px";
menu.style.zIndex = "100";

function btn(tekst, t) {
  let b = document.createElement("button");
  b.innerText = tekst;
  b.style.padding = "10px 20px";
  b.style.cursor = "pointer";
  b.onclick = function () {
    tryb = t;
    hvr = -1;
    kx = 0;
    ky = 0;
    zoom = 1.0;
    rysuj();
  };
  return b;
}

menu.appendChild(btn("Widok Mapy", "mapa"));
menu.appendChild(btn("Algorytm Parowania", "parowanie"));
menu.appendChild(btn("Trasa Księcia", "trasa_ksiecia"));
document.body.appendChild(menu);

let listaDomkow = [];
let listaKopalni = [];
let pionowyOdstep = 60;

function okno() {
  c.width = window.innerWidth;
  c.height = window.innerHeight;
  rysuj();
}
window.onresize = okno;
okno();

function dajCzystyIndeks(v) {
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    let m = v.match(/\d+/);
    return m ? parseInt(m[0]) : v;
  }
  if (v.indeks !== undefined) return dajCzystyIndeks(v.indeks);
  return v;
}

async function wczytaj() {
  let resDane = await fetch("dane.json");
  dane = await resDane.json();
  let resWyniki = await fetch("wyniki_algorytmy.json");
  wynikiAlgorytmy = await resWyniki.json();

  listaDomkow = [];
  listaKopalni = [];
  mapa = {};

  dane.forEach(function (p) {
    mapa[p.indeks] = p;
    if (p.typ == "Domek") listaDomkow.push(p);
    if (p.typ == "Kopalnia") listaKopalni.push(p);
  });

  if (wynikiAlgorytmy.parowanie) {
    wynikiAlgorytmy.parowanie.forEach(function (p) {
      let dIdx = dajCzystyIndeks(p.domek_indeks);
      let kIdx = dajCzystyIndeks(p.kopalnia_indeks);
      slownikParowania[dIdx] = kIdx;
    });
  }

  if (wynikiAlgorytmy.trasa_ksiecia) {
    let trasa =
      wynikiAlgorytmy.trasa_ksiecia.kolejnosc_kopalni_indeksy ||
      wynikiAlgorytmy.trasa_ksiecia;
    trasaKsiecia = trasa.map(dajCzystyIndeks);
  }
  rysuj();
}

im1.onload = im2.onload = function () {
  if (im1.complete && im2.complete) wczytaj();
};

c.onmousedown = function (e) {
  klik = true;
  sx = e.clientX - kx;
  sy = e.clientY - ky;
};
c.onmouseup = function () {
  klik = false;
};

c.onmousemove = function (e) {
  if (klik) {
    if (tryb == "mapa" || tryb == "trasa_ksiecia") {
      kx = e.clientX - sx;
      ky = e.clientY - sy;
    } else {
      ky = e.clientY - sy;
    }
  }
  hvr = -1;
  if (tryb == "mapa" || tryb == "trasa_ksiecia") {
    let mx = (e.clientX - kx) / zoom;
    let my = (e.clientY - ky) / zoom;
    dane.forEach(function (p) {
      if (Math.hypot(p.x * sk - mx, p.y * sk - my) < 25 / zoom) hvr = p.indeks;
    });
  } else {
    listaDomkow.forEach(function (d, i) {
      if (
        Math.hypot(e.clientX - 150, e.clientY - (ky + 80 + i * pionowyOdstep)) <
        25
      )
        hvr = d.indeks;
    });
    listaKopalni.forEach(function (k, i) {
      if (
        Math.hypot(
          e.clientX - (c.width - 150),
          e.clientY - (ky + 80 + i * pionowyOdstep),
        ) < 25
      )
        hvr = k.indeks;
    });
  }
  rysuj();
};

c.onwheel = function (e) {
  e.preventDefault();
  if (tryb == "mapa" || tryb == "trasa_ksiecia") {
    let posX = (e.clientX - kx) / zoom;
    let posY = (e.clientY - ky) / zoom;
    zoom = e.deltaY > 0 ? zoom * 0.9 : zoom * 1.1;
    kx = e.clientX - posX * zoom;
    ky = e.clientY - posY * zoom;
  } else {
    ky = ky - e.deltaY;
  }
  rysuj();
};

function rysuj() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, c.width, c.height);
  if (tryb == "mapa") rysujMape();
  else if (tryb == "parowanie") rysujParowanie();
  else rysujTrase();
}

function rysujMape() {
  ctx.translate(kx, ky);
  ctx.scale(zoom, zoom);
  let sizeH = 40 / zoom,
    sizeM = 60 / zoom;

  listaDomkow.forEach(function (d) {
    listaKopalni.forEach(function (k) {
      let polaczone = String(slownikParowania[d.indeks]) === String(k.indeks);
      let dotyczyHovera =
        hvr != -1 &&
        (String(hvr) === String(d.indeks) || String(hvr) === String(k.indeks));
      ctx.beginPath();
      ctx.moveTo(d.x * sk, d.y * sk);
      ctx.lineTo(k.x * sk, k.y * sk);
      let alpha =
        hvr != -1 && polaczone && dotyczyHovera
          ? 0.8
          : d.preferencja == k.zloze
            ? 0.1
            : 0.03;
      ctx.strokeStyle =
        "rgba(" +
        (d.preferencja == k.zloze ? "0, 255, 0" : "255, 255, 255") +
        ", " +
        alpha +
        ")";
      ctx.lineWidth = polaczone && dotyczyHovera ? 3 / zoom : 1 / zoom;
      ctx.stroke();
    });
  });

  dane.forEach(function (p) {
    let pID = String(p.indeks);
    let isHovered = String(hvr) === pID;
    let isPartnerHighlighted = false;
    if (hvr != -1 && mapa[hvr]) {
      if (
        mapa[hvr].typ === "Domek" &&
        p.typ === "Kopalnia" &&
        String(slownikParowania[hvr]) === pID
      )
        isPartnerHighlighted = true;
      if (
        mapa[hvr].typ === "Kopalnia" &&
        p.typ === "Domek" &&
        String(slownikParowania[p.indeks]) === String(hvr)
      )
        isPartnerHighlighted = true;
    }
    ctx.globalAlpha =
      hvr != -1 && !(isHovered || isPartnerHighlighted) ? 0.3 : 1.0;
    let s = p.typ == "Domek" ? sizeH : sizeM;
    let img = p.typ == "Domek" ? im1 : im2;
    ctx.drawImage(img, p.x * sk - s / 2, p.y * sk - s / 2, s, s);
    ctx.globalAlpha = 1.0;
    if (String(hvr) === pID) {
      ctx.fillStyle = "yellow";
      ctx.font = 16 / zoom + "px Arial";
      let text =
        p.indeks +
        (p.typ == "Domek"
          ? " (Pref: " + p.preferencja + ")"
          : " (Poj: " + p.pojemnosc + ", Złoże: " + p.zloze + ")");
      ctx.fillText(text, p.x * sk, p.y * sk + s / 2 + 16 / zoom);
    }
  });
}

function rysujParowanie() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, c.width, c.height);
  ctx.translate(0, ky);
  let dX = 150,
    kX = c.width - 150,
    iconSize = 25,
    offset = iconSize / 2,
    margin = 40,
    padding = 15;
  ctx.textBaseline = "middle";
  let ghosts = [];

  listaDomkow.forEach(function (domek, i) {
    let dY = 80 + i * pionowyOdstep;
    let kopalnieDlaDomku = listaKopalni.filter(
      (k) => String(slownikParowania[domek.indeks]) == String(k.indeks),
    );
    let pod =
      hvr == domek.indeks || kopalnieDlaDomku.some((k) => k.indeks == hvr);
    kopalnieDlaDomku.forEach((kopalnia) => {
      let kY = 80 + listaKopalni.indexOf(kopalnia) * pionowyOdstep;
      ctx.beginPath();
      ctx.moveTo(dX + offset, dY);
      ctx.lineTo(kX - offset, kY);
      ctx.strokeStyle = pod
        ? "yellow"
        : domek.preferencja == kopalnia.zloze
          ? "rgba(0, 255, 0, 0.2)"
          : "rgba(255, 255, 255, 0.1)";
      ctx.lineWidth = pod ? 5 : 2;
      ctx.stroke();
    });
    if (dY + ky >= 0 && dY + ky <= c.height) {
      ctx.drawImage(im1, dX - offset, dY - offset, iconSize, iconSize);
      ctx.fillStyle = pod ? "yellow" : "white";
      ctx.font = pod ? "bold 16px Arial" : "12px Arial";
      ctx.textAlign = "left";
      ctx.fillText(
        "Domek " + domek.indeks + " (Pref: " + domek.preferencja + ")",
        dX + offset + 10,
        dY,
      );
    } else if (pod) ghosts.push({ type: "domek", data: domek, y: dY + ky });
  });

  listaKopalni.forEach(function (kopalnia, i) {
    let kY = 80 + i * pionowyOdstep;
    let screenKY = kY + ky;
    let pod =
      hvr == kopalnia.indeks || slownikParowania[hvr] == kopalnia.indeks;
    if (screenKY >= 0 && screenKY <= c.height) {
      ctx.drawImage(im2, kX - offset, kY - offset, iconSize, iconSize);
      ctx.fillStyle = pod ? "yellow" : "white";
      ctx.font = pod ? "bold 16px Arial" : "12px Arial";
      ctx.textAlign = "right";
      ctx.fillText(
        kopalnia.zloze +
          " " +
          kopalnia.indeks +
          " (Poj: " +
          kopalnia.pojemnosc +
          ")",
        kX - offset - 10,
        kY,
      );
    } else if (pod)
      ghosts.push({ type: "kopalnia", data: kopalnia, y: kY + ky });
  });

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  let topStack = 0,
    bottomStack = 0;
  ghosts.forEach((g) => {
    let isTop = g.y < 0;
    let text =
      g.type == "domek"
        ? "Domek " + g.data.indeks + " (Pref: " + g.data.preferencja + ")"
        : g.data.zloze +
          " " +
          g.data.indeks +
          " (Poj: " +
          g.data.pojemnosc +
          ")";
    ctx.font = "bold 14px Arial";
    let textWidth = ctx.measureText(text).width,
      boxWidth = textWidth + iconSize + padding * 2;
    let x = g.type == "domek" ? margin : c.width - boxWidth - margin;
    let y = isTop
      ? margin + topStack * 35
      : c.height - margin - bottomStack * 35;
    ctx.fillStyle = "rgba(0, 0, 0, 0.9)";
    ctx.fillRect(x, y - offset, boxWidth, iconSize + 5);
    let iconX =
      g.type == "domek" ? x + padding : x + boxWidth - iconSize - padding;
    ctx.drawImage(
      g.type == "domek" ? im1 : im2,
      iconX,
      y - offset,
      iconSize,
      iconSize,
    );
    ctx.fillStyle = "yellow";
    ctx.textAlign = "left";
    ctx.fillText(
      text,
      g.type == "domek" ? iconX + iconSize + 5 : x + padding,
      y,
    );
    if (isTop) topStack++;
    else bottomStack++;
  });
}

function rysujTrase() {
  ctx.translate(kx, ky);
  ctx.scale(zoom, zoom);
  let sizeH = 25 / zoom,
    sizeM = 40 / zoom,
    sizeRouteM = 75 / zoom;

  dane.forEach(function (p) {
    ctx.globalAlpha = p.typ == "Domek" ? 0.2 : 0.4;
    let s = p.typ == "Domek" ? sizeH : sizeM;
    ctx.drawImage(
      p.typ == "Domek" ? im1 : im2,
      p.x * sk - s / 2,
      p.y * sk - s / 2,
      s,
      s,
    );
    ctx.globalAlpha = 1.0;
  });

  let totalDist = 0;
  if (trasaKsiecia.length > 1) {
    ctx.beginPath();
    trasaKsiecia.forEach(function (idx, i) {
      let p = mapa[idx];
      if (p)
        i == 0
          ? ctx.moveTo(p.x * sk, p.y * sk)
          : ctx.lineTo(p.x * sk, p.y * sk);
    });
    let start = mapa[trasaKsiecia[0]];
    if (start) ctx.lineTo(start.x * sk, start.y * sk);
    ctx.strokeStyle = "cyan";
    ctx.lineWidth = 5 / zoom;
    ctx.lineJoin = "round";
    ctx.stroke();
    ctx.fillStyle = "yellow";
    ctx.font = 16 / zoom + "px Arial";
    ctx.textAlign = "center";
    for (let i = 0; i < trasaKsiecia.length; i++) {
      let p1 = mapa[trasaKsiecia[i]],
        p2 = mapa[trasaKsiecia[(i + 1) % trasaKsiecia.length]];
      if (p1 && p2) {
        let segDist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
        totalDist += segDist;
        ctx.fillText(
          segDist.toFixed(1),
          ((p1.x + p2.x) * sk) / 2,
          ((p1.y + p2.y) * sk) / 2 - 8 / zoom,
        );
      }
    }
  }

  trasaKsiecia.forEach(function (idx, i) {
    let p = mapa[idx];
    if (p) {
      ctx.drawImage(
        im2,
        p.x * sk - sizeRouteM / 2,
        p.y * sk - sizeRouteM / 2,
        sizeRouteM,
        sizeRouteM,
      );
      ctx.fillStyle = "white";
      ctx.font = "bold " + 18 / zoom + "px Arial";
      ctx.fillText(
        i + 1,
        p.x * sk + sizeRouteM / 2 + 5 / zoom,
        p.y * sk - sizeRouteM / 2,
      );
    }
  });

  let finalDist =
    wynikiAlgorytmy.trasa_ksiecia && wynikiAlgorytmy.trasa_ksiecia.dlugosc
      ? wynikiAlgorytmy.trasa_ksiecia.dlugosc
      : totalDist;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = "yellow";
  ctx.font = "bold 20px Arial";
  ctx.fillText("Całkowita odległość trasy: " + finalDist.toFixed(1), 20, 40);
}
