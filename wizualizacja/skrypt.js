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
  if (typeof v === "number") {
    return v;
  }
  if (typeof v === "string") {
    let m = v.match(/\d+/);
    if (m) {
      return parseInt(m[0]);
    } else {
      return v;
    }
  }
  if (v.indeks !== undefined) {
    return dajCzystyIndeks(v.indeks);
  }
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
    if (p.typ == "Domek") {
      listaDomkow.push(p);
    }
    if (p.typ == "Kopalnia") {
      listaKopalni.push(p);
    }
  });

  if (wynikiAlgorytmy.parowanie) {
    wynikiAlgorytmy.parowanie.forEach(function (p) {
      let dIdx = dajCzystyIndeks(p.domek_indeks);
      let kIdx = dajCzystyIndeks(p.kopalnia_indeks);
      slownikParowania[dIdx] = kIdx;
    });
  }

  if (wynikiAlgorytmy.trasa_ksiecia) {
    let trasa = wynikiAlgorytmy.trasa_ksiecia.kolejnosc_kopalni_indeksy;
    if (!trasa) {
      trasa = wynikiAlgorytmy.trasa_ksiecia;
    }
    trasaKsiecia = trasa.map(dajCzystyIndeks);
  }

  rysuj();
}

im1.onload = function () {
  if (im1.complete && im2.complete) {
    wczytaj();
  }
};
im2.onload = function () {
  if (im1.complete && im2.complete) {
    wczytaj();
  }
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
    let hitRadius = 25 / zoom;

    dane.forEach(function (p) {
      let dX = p.x * sk - mx;
      let dY = p.y * sk - my;
      let dist = Math.hypot(dX, dY);
      if (dist < hitRadius) {
        hvr = p.indeks;
      }
    });
  } else {
    listaDomkow.forEach(function (d, i) {
      let targetX = 150;
      let targetY = ky + 80 + i * pionowyOdstep;
      let dist = Math.hypot(e.clientX - targetX, e.clientY - targetY);
      if (dist < 25) {
        hvr = d.indeks;
      }
    });

    listaKopalni.forEach(function (k, i) {
      let targetX = c.width - 150;
      let targetY = ky + 80 + i * pionowyOdstep;
      let dist = Math.hypot(e.clientX - targetX, e.clientY - targetY);
      if (dist < 25) {
        hvr = k.indeks;
      }
    });
  }
  rysuj();
};

c.onwheel = function (e) {
  e.preventDefault();
  if (tryb == "mapa" || tryb == "trasa_ksiecia") {
    let posX = (e.clientX - kx) / zoom;
    let posY = (e.clientY - ky) / zoom;

    if (e.deltaY > 0) {
      zoom = zoom * 0.9;
    } else {
      zoom = zoom * 1.1;
    }

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

  if (tryb == "mapa") {
    rysujMape();
  } else if (tryb == "parowanie") {
    rysujParowanie();
  } else {
    rysujTrase();
  }
}

function rysujMape() {
  ctx.translate(kx, ky);
  ctx.scale(zoom, zoom);

  let sizeH = 40 / zoom;
  let sizeM = 60 / zoom;

  listaDomkow.forEach(function (d) {
    listaKopalni.forEach(function (k) {
      ctx.beginPath();
      ctx.moveTo(d.x * sk, d.y * sk);
      ctx.lineTo(k.x * sk, k.y * sk);

      let pod = false;
      if (hvr == d.indeks || hvr == k.indeks) {
        pod = true;
      }

      if (d.preferencja == k.zloze) {
        if (pod) {
          ctx.strokeStyle = "rgba(0, 255, 0, 0.8)";
        } else {
          ctx.strokeStyle = "rgba(0, 255, 0, 0.1)";
        }
      } else {
        if (pod) {
          ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
        } else {
          ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
        }
      }

      if (pod) {
        ctx.lineWidth = 3 / zoom;
      } else {
        ctx.lineWidth = 1 / zoom;
      }
      ctx.stroke();
    });
  });

  dane.forEach(function (p) {
    let s;
    let img;

    if (p.typ == "Domek") {
      s = sizeH;
      img = im1;
    } else {
      s = sizeM;
      img = im2;
    }

    let off = s / 2;
    ctx.drawImage(img, p.x * sk - off, p.y * sk - off, s, s);

    if (hvr == p.indeks) {
      ctx.fillStyle = "yellow";
      ctx.font = 16 / zoom + "px Arial";
      ctx.fillText(p.indeks, p.x * sk, p.y * sk + off + 16 / zoom);
    }
  });
}

function rysujParowanie() {
  ctx.translate(0, ky);
  let dX = 150;
  let kX = c.width - 150;

  ctx.font = "16px Arial";

  listaDomkow.forEach(function (domek, i) {
    let dY = 80 + i * pionowyOdstep;
    let kIdx = slownikParowania[domek.indeks];

    let kopalnia = listaKopalni.find(function (k) {
      return k.indeks == kIdx;
    });

    let text = "Domek " + domek.indeks;

    if (kopalnia) {
      let index = listaKopalni.indexOf(kopalnia);
      let kY = 80 + index * pionowyOdstep;

      let pod = false;
      if (hvr == domek.indeks || hvr == kopalnia.indeks) {
        pod = true;
      }

      if (pod) {
        let dist = Math.hypot(
          domek.x - kopalnia.x,
          domek.y - kopalnia.y,
        ).toFixed(1);
        text += " (Dystans: " + dist + ")";
      }

      ctx.beginPath();
      ctx.moveTo(dX + 20, dY);
      ctx.lineTo(kX - 20, kY);

      if (domek.preferencja == kopalnia.zloze) {
        if (pod) {
          ctx.strokeStyle = "lime";
        } else {
          ctx.strokeStyle = "rgba(0, 255, 0, 0.5)";
        }
      } else {
        if (pod) {
          ctx.strokeStyle = "white";
        } else {
          ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
        }
      }

      if (pod) {
        ctx.lineWidth = 4;
      } else {
        ctx.lineWidth = 2;
      }
      ctx.stroke();
    }

    ctx.drawImage(im1, dX - 20, dY - 20, 40, 40);

    if (hvr == domek.indeks) {
      ctx.fillStyle = "yellow";
    } else {
      ctx.fillStyle = "white";
    }

    ctx.textAlign = "left";
    ctx.fillText(text, dX + 30, dY + 5);
  });

  listaKopalni.forEach(function (kopalnia, i) {
    let kY = 80 + i * pionowyOdstep;
    ctx.drawImage(im2, kX - 20, kY - 20, 40, 40);

    if (hvr == kopalnia.indeks) {
      ctx.fillStyle = "yellow";
    } else {
      ctx.fillStyle = "white";
    }

    ctx.textAlign = "right";
    let napis =
      kopalnia.zloze +
      " " +
      kopalnia.indeks +
      " (Poj: " +
      kopalnia.pojemnosc +
      ")";
    ctx.fillText(napis, kX - 30, kY + 5);
  });

  ctx.textAlign = "left";
}

function rysujTrase() {
  ctx.translate(kx, ky);
  ctx.scale(zoom, zoom);

  let sizeH = 25 / zoom;
  let sizeM = 40 / zoom;
  let sizeRouteM = 75 / zoom;

  dane.forEach(function (p) {
    if (p.typ == "Domek") {
      ctx.globalAlpha = 0.2;
    } else {
      ctx.globalAlpha = 0.4;
    }

    let s;
    let img;

    if (p.typ == "Domek") {
      s = sizeH;
      img = im1;
    } else {
      s = sizeM;
      img = im2;
    }

    let off = s / 2;
    ctx.drawImage(img, p.x * sk - off, p.y * sk - off, s, s);
    ctx.globalAlpha = 1.0;
  });

  let totalDist = 0;

  if (trasaKsiecia.length > 1) {
    ctx.beginPath();

    trasaKsiecia.forEach(function (idx, i) {
      let p = mapa[idx];
      if (p) {
        if (i == 0) {
          ctx.moveTo(p.x * sk, p.y * sk);
        } else {
          ctx.lineTo(p.x * sk, p.y * sk);
        }
      }
    });

    let start = mapa[trasaKsiecia[0]];
    if (start) {
      ctx.lineTo(start.x * sk, start.y * sk);
    }

    ctx.strokeStyle = "cyan";
    ctx.lineWidth = 5 / zoom;
    ctx.lineJoin = "round";
    ctx.stroke();

    ctx.fillStyle = "yellow";
    ctx.font = 16 / zoom + "px Arial";
    ctx.textAlign = "center";

    for (let i = 0; i < trasaKsiecia.length; i++) {
      let p1 = mapa[trasaKsiecia[i]];
      let nx = (i + 1) % trasaKsiecia.length;
      let p2 = mapa[trasaKsiecia[nx]];

      if (p1 && p2) {
        let segmentDist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
        totalDist = totalDist + segmentDist;
        let midX = ((p1.x + p2.x) * sk) / 2;
        let midY = ((p1.y + p2.y) * sk) / 2;
        ctx.fillText(segmentDist.toFixed(1), midX, midY - 8 / zoom);
      }
    }
    ctx.textAlign = "left";
  }

  trasaKsiecia.forEach(function (idx, i) {
    let p = mapa[idx];
    if (p) {
      let s = sizeRouteM;
      let off = s / 2;
      ctx.drawImage(im2, p.x * sk - off, p.y * sk - off, s, s);
      ctx.fillStyle = "white";
      ctx.font = "bold " + 18 / zoom + "px Arial";
      ctx.fillText(i + 1, p.x * sk + off + 5 / zoom, p.y * sk - off);
    }
  });

  let finalDist;
  if (wynikiAlgorytmy.trasa_ksiecia && wynikiAlgorytmy.trasa_ksiecia.dlugosc) {
    finalDist = wynikiAlgorytmy.trasa_ksiecia.dlugosc;
  } else {
    finalDist = totalDist;
  }

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = "yellow";
  ctx.font = "bold 20px Arial";
  ctx.fillText("Całkowita odległość trasy: " + finalDist.toFixed(1), 20, 40);
}
