var c = document.getElementById("projekt_canvas");
var ctx = c.getContext("2d");

var dane = [];
var mapa = {};
var zasieg = 3;
var zoom = 1.0;
var kx = 0;
var ky = 0;
var klik = false;
var sx, sy;
var hvr = -1;

var sk = 60;
var im1 = new Image();
im1.src = "domek.png";
var im2 = new Image();
im2.src = "kopalnia.png";

//dopasowanie do ekranu

function okno() {
  c.width = window.innerWidth;
  c.height = window.innerHeight;
  rysuj();
}
window.onresize = okno;
okno();

//dane z jsona

async function wczytaj() {
  var odp = await fetch("dane.json");
  dane = await odp.json();

  for (var i = 0; i < dane.length; i++) {
    mapa[dane[i].indeks] = dane[i];
  }

  rysuj();
}

var zal = 0;
im1.onload = im2.onload = function () {
  zal++;
  if (zal == 2) wczytaj();
};

//ruszanie po mapie

function ekranNaSwiat(x, y) {
  return {
    x: (x - kx) / zoom,
    y: (y - ky) / zoom,
  };
}

c.onmousedown = function (e) {
  klik = true;
  sx = e.clientX - kx;
  sy = e.clientY - ky;
};

c.onmousemove = function (e) {
  if (klik == true) {
    kx = e.clientX - sx;
    ky = e.clientY - sy;
  }

  var pos = ekranNaSwiat(e.clientX, e.clientY);

  hvr = -1;
  for (var i = 0; i < dane.length; i++) {
    var p = dane[i];
    if (p.typ != "Domek") continue;

    var dx = p.x * sk - pos.x;
    var dy = p.y * sk - pos.y;

    if (dx * dx + dy * dy < 25 * 25) {
      hvr = p.indeks;
      break;
    }
  }

  rysuj();
};

window.onmouseup = function () {
  klik = false;
};

c.onwheel = function (e) {
  e.preventDefault();

  var pos = ekranNaSwiat(e.clientX, e.clientY);

  var s = e.deltaY > 0 ? 0.9 : 1.1;
  zoom = zoom * s;

  kx = e.clientX - pos.x * zoom;
  ky = e.clientY - pos.y * zoom;

  rysuj();
};

//glowna funkcja

function rysuj() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, c.width, c.height);
  ctx.translate(kx, ky);
  ctx.scale(zoom, zoom);

  //drogi

  for (var i = 0; i < dane.length; i++) {
    var p = dane[i];
    if (p.typ != "Domek") continue;

    var x1 = p.x * sk;
    var y1 = p.y * sk;

    var kopalnie = [];
    for (var j = 0; j < p.sasiedzi.length; j++) {
      var s = p.sasiedzi[j];
      var znaleziony = mapa[s.indeks];
      if (znaleziony) {
        kopalnie.push({ pkt: znaleziony, d: s.odleglosc });
      }
    }

    if (kopalnie.length > 0) {
      var bliskie = [];
      for (var j = 0; j < kopalnie.length; j++) {
        if (kopalnie[j].d < zasieg) bliskie.push(kopalnie[j]);
      }

      if (bliskie.length > 0) {
        for (var j = 0; j < bliskie.length; j++) {
          rysujLinie(p, bliskie[j], false);
        }
      } else {
        kopalnie.sort(function (a, b) {
          return a.d - b.d;
        });
        rysujLinie(p, kopalnie[0], true);
      }
    }
  }

  //domki i kopalnie

  for (var i = 0; i < dane.length; i++) {
    var p = dane[i];
    var px = p.x * sk;
    var py = p.y * sk;

    if (hvr == p.indeks && p.typ == "Domek") {
      ctx.shadowColor = "white";
      ctx.shadowBlur = 15;
      c.style.cursor = "pointer";
    }

    if (p.typ == "Domek") {
      ctx.drawImage(im1, px - 15, py - 15, 30, 30);
    } else {
      ctx.drawImage(im2, px - 15, py - 15, 30, 30);
    }

    ctx.shadowBlur = 0;

    if (hvr == p.indeks || p.typ == "Kopalnia") {
      ctx.fillStyle = "white";
      ctx.font = "bold 12px Arial";
      ctx.textAlign = "center";
      var t = p.typ == "Domek" ? "Chce: " + p.preferencja : p.zloze;
      ctx.fillText(t, px, py + 30);
    }
  }

  if (hvr == -1) c.style.cursor = "default";
}

function rysujLinie(p, kop, przerywana) {
  var x1 = p.x * sk;
  var y1 = p.y * sk;
  var x2 = kop.pkt.x * sk;
  var y2 = kop.pkt.y * sk;

  var pod = hvr == p.indeks;

  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);

  if (przerywana) ctx.setLineDash([5, 5]);

  if (kop.pkt.zloze == p.preferencja) {
    ctx.strokeStyle = pod ? "rgba(0, 255, 0, 1)" : "rgba(0, 255, 0, 0.2)";
  } else {
    ctx.strokeStyle = pod
      ? "rgba(255, 255, 255, 0.8)"
      : "rgba(255, 255, 255, 0.1)";
  }

  ctx.lineWidth = pod ? 3 : 1;
  ctx.stroke();
  ctx.setLineDash([]);
}

//wczytałem dane z tego testowego jsona i stworzyłem powiedzmy mapę tego co jest. Drogi są rysowane na podstawie odległości, u góry jest zmienna zasieg narazie ustawiona na 3
//szuka kopalni w odległości maximum 3 jeżeli jest preferowany surowiec to droga zaznacza się na zielono dodatkowo jeżeli nie będzie żadnej kopalni w tym zasięgu to szuka pierwszej
//która jest najbliżej. Skoro motyw minecraftowy to motyw minecraftowy, zrobiłem cały system poruszania się i zoomowania który dalej ma swoje bolączki mimo pomocy miłych kolegów,
//dalej trzeba powalczyć
