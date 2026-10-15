/* YK Property Services — shared site script */
(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const WA = '17055008455';
  const EMAIL = 'servicesykproperty@gmail.com';
  const PHONE = '+17055008455';

  /* ==========================================================
     Customer reviews — add REAL, verified reviews here only.
     Example: { text: '...', name: 'Jordan M.', detail: 'Rental turnover · Range Lake' }
     ========================================================== */
  const REVIEWS = [];

  $$('.js-year').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ---------- Seeded random ---------- */
  function rng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

  /* ---------- Header: scrolled state, dropdown, mobile menu ---------- */
  const nav = $('#nav');
  const dd = $('.dd');
  if (dd) {
    const btn = $('.dd-btn', dd);
    const set = open => { dd.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); };
    btn.addEventListener('click', e => { e.stopPropagation(); set(!dd.classList.contains('open')); });
    if (finePointer) {
      let t;
      dd.addEventListener('mouseenter', () => { clearTimeout(t); set(true); });
      dd.addEventListener('mouseleave', () => { t = setTimeout(() => set(false), 180); });
    }
    document.addEventListener('click', e => { if (!dd.contains(e.target)) set(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); } });
  }
  const menuBtn = $('#menuBtn');
  if (menuBtn) {
    const setMenu = open => {
      document.body.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', open);
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (nav) nav.classList.toggle('scrolled', open || window.scrollY > 30);
    };
    menuBtn.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    $$('#mnav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------- Spruce tree lines ---------- */
  function spruce(x, base, h, r) {
    const tiers = Math.max(4, Math.round(h / 15));
    const maxW = h * (0.2 + r() * 0.08);
    const step = h / tiers;
    const L = [[x, base - h]], R = [];
    for (let j = 1; j <= tiers; j++) {
      const y = base - h + j * step;
      const w = maxW * (j / tiers) * (0.8 + r() * 0.35) + 1.5;
      L.push([x - w, y]);
      R.push([x + w * (0.85 + r() * 0.3), y]);
      if (j < tiers) { L.push([x - w * 0.42, y - step * 0.08]); R.push([x + w * 0.42, y - step * 0.08]); }
    }
    L.push([x - 1.6, base + 4]);
    R.push([x + 1.6, base + 4]);
    const pts = L.concat(R.reverse());
    return 'M' + pts.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z';
  }
  function treeline(svg, opts) {
    const r = rng(opts.seed);
    let d = '';
    for (let x = -20; x < 1470;) {
      const h = opts.minH + r() * (opts.maxH - opts.minH);
      d += spruce(x, opts.base + r() * 5, h, r);
      x += opts.gap + r() * opts.gapVar;
      if (r() < opts.clearing) x += 40 + r() * 70;
    }
    const ns = 'http://www.w3.org/2000/svg';
    const ground = document.createElementNS(ns, 'path');
    ground.setAttribute('d', `M0 ${opts.base} H1440 V220 H0Z`);
    ground.setAttribute('fill', opts.fill);
    const trees = document.createElementNS(ns, 'path');
    trees.setAttribute('d', d);
    trees.setAttribute('fill', opts.fill);
    svg.append(ground, trees);
    if (opts.snow) {
      const s = document.createElementNS(ns, 'path');
      s.setAttribute('d', 'M0 207C260 196 470 214 760 203S1190 195 1440 205V220H0Z');
      s.setAttribute('fill', opts.snow);
      svg.append(s);
    }
  }
  const hero = $('.hero');
  const farSvg = $('#treesFar');
  const nearSvg = $('#treesNear');
  const seedOff = Number(hero && hero.dataset.seed) || 0;
  if (farSvg) treeline(farSvg, { seed: 7 + seedOff, base: 196, minH: 28, maxH: 82, gap: 9, gapVar: 14, clearing: .05, fill: '#14336E' });
  if (nearSvg) treeline(nearSvg, { seed: 21 + seedOff, base: 206, minH: 55, maxH: 165, gap: 15, gapVar: 30, clearing: .12, fill: '#050F26', snow: (hero && hero.dataset.snow) || '#EEF3F9' });

  /* ---------- Aurora + stars + snow (hero canvases) ---------- */
  const A = $('#aurora');
  const S = $('#sky');
  let heroVisible = true, rafId = 0;
  if (A && S && hero) {
    const ax = A.getContext('2d');
    let aw = 0, ah = 0;
    const bands = [
      { c: [78, 240, 184], y: .34, amp: .07, th: .30, f: 1.4, s: 1.0, ph: 0, a: .8 },
      { c: [60, 205, 255], y: .24, amp: .06, th: .20, f: 2.2, s: -.8, ph: 2, a: .45 },
      { c: [150, 110, 255], y: .44, amp: .06, th: .18, f: 1.1, s: .6, ph: 4, a: .42 },
      { c: [110, 255, 160], y: .18, amp: .05, th: .14, f: 3.0, s: 1.3, ph: 1, a: .4 }
    ];
    const sizeAurora = () => {
      const r = A.getBoundingClientRect();
      aw = A.width = Math.max(1, Math.round(r.width / 2));
      ah = A.height = Math.max(1, Math.round(r.height / 2));
    };
    const drawAurora = t => {
      const k = t * 0.00012;
      ax.clearRect(0, 0, aw, ah);
      ax.globalCompositeOperation = 'lighter';
      const steps = Math.min(90, Math.round(aw / 6));
      const sw = aw / steps + 1;
      for (const b of bands) {
        const [cr, cg, cb] = b.c;
        for (let i = 0; i <= steps; i++) {
          const u = i / steps;
          const x = u * aw;
          const y = (b.y + Math.sin(u * b.f * 6.283 + k * b.s * 6 + b.ph) * b.amp + Math.sin(u * b.f * 13.1 + k * b.s * 9 + b.ph * 1.7) * b.amp * .35) * ah;
          const th = b.th * ah * (0.55 + 0.45 * Math.sin(u * 5.3 + k * b.s * 4 + b.ph));
          const ray = 0.55 + 0.45 * Math.sin(u * 47 + k * 11 + b.ph * 3) * Math.sin(u * 19 - k * 7);
          const a = b.a * ray;
          const g = ax.createLinearGradient(0, y - th, 0, y + th * 0.08);
          g.addColorStop(0, 'rgba(150,100,255,0)');
          g.addColorStop(0.45, `rgba(${cr},${cg},${cb},${a * 0.35})`);
          g.addColorStop(0.9, `rgba(${cr},${cg},${cb},${a})`);
          g.addColorStop(1, `rgba(${cr},${cg},${cb},0)`);
          ax.fillStyle = g;
          ax.fillRect(x, y - th, sw, th * 1.08);
        }
      }
    };
    const sx = S.getContext('2d');
    let sw2 = 0, sh2 = 0, dpr = 1, stars = [], flakes = [];
    const newFlake = anywhere => {
      const z = Math.random();
      return { x: Math.random() * sw2, y: anywhere ? Math.random() * sh2 : -10, r: .6 + z * 2.2, vy: .25 + z * .9, vx: (Math.random() - .5) * .3, p: Math.random() * 6.28, a: .35 + z * .55 };
    };
    const sizeSky = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      const r = S.getBoundingClientRect();
      sw2 = r.width; sh2 = r.height;
      S.width = Math.round(sw2 * dpr); S.height = Math.round(sh2 * dpr);
      sx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const r1 = rng(99);
      stars = Array.from({ length: Math.round(sw2 / 9) }, () => ({ x: r1() * sw2, y: r1() * sh2 * 0.6, r: r1() * 1.1 + .3, p: r1() * 6.28, s: .5 + r1() * 1.5 }));
      flakes = Array.from({ length: Math.min(140, Math.round(sw2 / 11)) }, () => newFlake(true));
    };
    const drawSky = t => {
      sx.clearRect(0, 0, sw2, sh2);
      for (const s of stars) {
        const a = 0.35 + 0.5 * (0.5 + 0.5 * Math.sin(t * 0.001 * s.s + s.p));
        sx.fillStyle = `rgba(230,240,255,${a})`;
        sx.beginPath(); sx.arc(s.x, s.y, s.r, 0, 6.283); sx.fill();
      }
      for (const f of flakes) {
        if (!reduce) {
          f.y += f.vy; f.x += f.vx + Math.sin(t * 0.0012 + f.p) * 0.35;
          if (f.y > sh2 + 10) Object.assign(f, newFlake(false));
          if (f.x > sw2 + 10) f.x = -10; else if (f.x < -10) f.x = sw2 + 10;
        }
        sx.fillStyle = `rgba(255,255,255,${f.a})`;
        sx.beginPath(); sx.arc(f.x, f.y, f.r, 0, 6.283); sx.fill();
      }
    };
    const frame = t => { drawAurora(t); drawSky(t); rafId = heroVisible && !reduce ? requestAnimationFrame(frame) : 0; };
    const resizeAll = () => { sizeAurora(); sizeSky(); if (reduce || !rafId) frame(performance.now()); };
    resizeAll();
    let rT; window.addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(resizeAll, 150); });
    new IntersectionObserver(([e]) => {
      heroVisible = e.isIntersecting;
      if (heroVisible && !rafId && !reduce) rafId = requestAnimationFrame(frame);
    }).observe(hero);
  }

  /* ---------- Floating WhatsApp button visibility ---------- */
  const fab = $('#fab');
  if (fab) {
    if (hero) new IntersectionObserver(([e]) => fab.classList.toggle('show', !e.isIntersecting)).observe(hero);
    else fab.classList.add('show');
  }

  /* ---------- Parallax and nav state ---------- */
  const heroInner = $('#heroInner');
  let ticking = false;
  function onScroll() {
    const y = window.scrollY;
    if (nav && !document.body.classList.contains('menu-open')) nav.classList.toggle('scrolled', y > 30);
    if (!reduce && hero && y < window.innerHeight * 1.2) {
      if (A) A.style.transform = `translateY(${y * 0.35}px)`;
      if (farSvg) farSvg.style.transform = `translateY(${y * 0.12}px)`;
      if (heroInner) {
        heroInner.style.transform = `translateY(${y * 0.22}px)`;
        heroInner.style.opacity = Math.max(0, 1 - y / (window.innerHeight * 0.85));
      }
    }
    ticking = false;
  }
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- Home hero paint-roller intro ---------- */
  const rollerSVG = '<svg class="roller" viewBox="0 0 74 150" aria-hidden="true">' +
    '<path d="M14 104v10h38v14" fill="none" stroke="#C9D3E2" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<rect x="44" y="124" width="16" height="26" rx="6" fill="#0B1E44" stroke="#2A4F9A" stroke-width="2"/>' +
    '<rect x="1" y="1" width="26" height="104" rx="11" fill="url(#nap)" stroke="#0F3A97" stroke-width="2"/>' +
    '<path d="M7 10v86" stroke="rgba(255,255,255,.35)" stroke-width="3" stroke-linecap="round"/></svg>';
  function startHero() {
    if (window.__heroStarted) return;
    window.__heroStarted = true;
    const root = document.documentElement;
    if (!root.classList.contains('anim-ready')) return;
    const lines = $$('.headline[data-roller] .line');
    let delay = 350;
    lines.forEach((ln, idx) => {
      ln.insertAdjacentHTML('beforeend', rollerSVG);
      const roller = $('.roller', ln);
      const w = ln.offsetWidth;
      const dur = Math.min(1250, Math.max(650, w * 1.25));
      const opts = { duration: dur, delay, easing: 'cubic-bezier(.55,.08,.3,1)', fill: 'both' };
      const reveal = [{ clipPath: 'inset(-25% 100% -25% 0)' }, { clipPath: 'inset(-25% 0% -25% 0)' }];
      $('.stroke', ln).animate(reveal, opts);
      $('.txt', ln).animate(reveal, opts);
      const last = idx === lines.length - 1;
      roller.animate([
        { transform: 'translateX(-10px) rotate(-10deg)', opacity: 0 },
        { transform: 'translateX(0) rotate(-4deg)', opacity: 1, offset: .08 },
        { transform: `translateX(${w}px) rotate(4deg)`, opacity: 1, offset: .9 },
        { transform: `translateX(${w + (last ? 60 : 10)}px) rotate(${last ? 14 : 6}deg)`, opacity: 0 }
      ], { ...opts, duration: dur * 1.08 });
      delay += dur - 90;
    });
    const after = { duration: 700, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'both' };
    const up = [{ opacity: 0, transform: 'translateY(14px)' }, { opacity: 1, transform: 'none' }];
    $$('.hero .lede, .hero .ctas, .hero .hero-meta').forEach((el, i) => el.animate(up, { ...after, delay: delay - 200 + i * 150 }));
  }
  if ($('.headline[data-roller]')) {
    if (document.fonts && document.fonts.ready) Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 1500))]).then(startHero);
    else startHero();
  }

  /* ---------- Scroll reveals ---------- */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      if (e.target.matches('.swatches, .svc-grid')) setTimeout(() => e.target.classList.add('settled'), 1400);
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal, .swatches, .svc-grid, .steps').forEach(el => io.observe(el));

  /* ---------- Swatch card tilt ---------- */
  if (finePointer && !reduce) {
    $$('.swatch').forEach(card => {
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.classList.add('tilting');
        card.style.transform = `rotateY(${(px - .5) * 10}deg) rotateX(${(.5 - py) * 8}deg) translateZ(10px)`;
        card.style.setProperty('--gx', px * 100 + '%');
        card.style.setProperty('--gy', py * 100 + '%');
      });
      card.addEventListener('pointerleave', () => { card.classList.remove('tilting'); card.style.transform = ''; });
    });
  }

  /* ==========================================================
     Before / after illustrations (SVG, 800 x 500)
     Illustrative only — swap for real job photos later by putting
     <img class="before"> and <img class="after"> inside a .ba element.
     ========================================================== */
  let uid = 0;
  const svgWrap = (cls, body, defs = '') => `<svg class="${cls}" viewBox="0 0 800 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>${defs}</defs>${body}</svg>`;
  const skyDefs = id => `<linearGradient id="sk${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#030B1F"/><stop offset="1" stop-color="#14336E"/></linearGradient>
    <linearGradient id="au${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4EF0B8" stop-opacity="0"/><stop offset=".7" stop-color="#4EF0B8" stop-opacity=".9"/><stop offset="1" stop-color="#4EF0B8" stop-opacity="0"/></linearGradient>`;
  function windowEl(id, x, y, w, h, frame, dirty) {
    const r = rng(x + y);
    let stars = '';
    for (let i = 0; i < 14; i++) stars += `<circle cx="${(x + 14 + r() * (w - 28)).toFixed(0)}" cy="${(y + 14 + r() * h * .45).toFixed(0)}" r="${(r() * 1.4 + .5).toFixed(1)}" fill="#fff" opacity=".8"/>`;
    const trees = `<path d="M${x + 10} ${y + h - 10} l14 -38 14 38z M${x + 30} ${y + h - 10} l18 -54 18 54z M${x + w - 70} ${y + h - 10} l16 -44 16 44z M${x + w - 44} ${y + h - 10} l17 -30 17 30z" fill="#050F26"/>`;
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="${frame}"/>
      <rect x="${x + 10}" y="${y + 10}" width="${w - 20}" height="${h - 20}" fill="url(#sk${id})"/>
      <path d="M${x + 10} ${y + h * .42} C${x + w * .3} ${y + h * .2} ${x + w * .55} ${y + h * .55} ${x + w - 10} ${y + h * .3} V${y + h * .55} C${x + w * .6} ${y + h * .75} ${x + w * .3} ${y + h * .45} ${x + 10} ${y + h * .62}Z" fill="url(#au${id})" opacity="${dirty ? .35 : .85}"/>
      ${stars}${trees}
      <rect x="${x + w / 2 - 4}" y="${y + 10}" width="8" height="${h - 20}" fill="${frame}"/>
      <rect x="${x + 10}" y="${y + h / 2 - 4}" width="${w - 20}" height="8" fill="${frame}"/>
      ${dirty ? `<rect x="${x + 10}" y="${y + 10}" width="${w - 20}" height="${h - 20}" fill="#9C8F6E" opacity=".35"/>` : ''}
      <rect x="${x - 10}" y="${y + h}" width="${w + 20}" height="12" rx="3" fill="${frame}"/>`;
  }
  const scuffs = (seed, n, x0, x1, y0, y1, c = '#5D5446') => { const r = rng(seed); let s = ''; for (let i = 0; i < n; i++) { const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0); s += `<path d="M${x.toFixed(0)} ${y.toFixed(0)} q${(10 + r() * 30).toFixed(0)} ${(-4 + r() * 8).toFixed(0)} ${(20 + r() * 40).toFixed(0)} ${(-2 + r() * 4).toFixed(0)}" stroke="${c}" stroke-width="${(2 + r() * 4).toFixed(1)}" stroke-linecap="round" fill="none" opacity="${(.25 + r() * .3).toFixed(2)}"/>`; } return s; };
  const hole = (x, y, s) => `<path d="M${x - 14 * s} ${y - 4 * s} l8 ${-10 * s} 12 ${2 * s} 10 ${-6 * s} 8 ${12 * s} -4 ${10 * s} 6 ${8 * s} -14 ${6 * s} -12 ${-4 * s} -10 ${2 * s} z" fill="#3A342C"/><path d="M${x - 6 * s} ${y - 2 * s} l6 ${-4 * s} 8 ${2 * s} 2 ${8 * s} -8 ${2 * s}z" fill="#1E1A15"/>`;
  const crack = (x, y) => `<path d="M${x} ${y} l12 18 -6 14 16 22 -4 18 14 20" stroke="#5D5446" stroke-width="2.4" fill="none" opacity=".7"/><path d="M${x + 18} ${y + 54} l18 6" stroke="#5D5446" stroke-width="1.8" fill="none" opacity=".6"/>`;
  const sparkle = (x, y, s, c = '#4EF0B8') => `<path transform="translate(${x} ${y}) scale(${s})" d="M10 0l2.4 7.6L20 10l-7.6 2.4L10 20l-2.4-7.6L0 10l7.6-2.4z" fill="${c}"/>`;
  const floor = (c, line, shine) => `<rect y="400" width="800" height="100" fill="${c}"/>${[430, 465].map(y => `<path d="M0 ${y}H800" stroke="${line}" stroke-width="2"/>`).join('')}${[120, 330, 560, 740].map((x, i) => `<path d="M${x} ${i % 2 ? 430 : 400}v35" stroke="${line}" stroke-width="2"/>`).join('')}${shine ? '<path d="M80 420 L300 420 L260 492 L40 492Z" fill="#fff" opacity=".12"/>' : ''}`;
  const plant = (x, y) => `<path d="M${x} ${y} c-30 -40 -10 -90 0 -110 c10 20 30 70 0 110z" fill="#127A62"/><path d="M${x} ${y} c-50 -20 -60 -60 -58 -80 c20 10 50 40 58 80z" fill="#1A9A79"/><path d="M${x} ${y} c50 -20 60 -60 58 -80 c-20 10 -50 40 -58 80z" fill="#1A9A79"/><path d="M${x - 24} ${y} h48 l-6 42 h-36z" fill="#0F2D66"/>`;

  const SCENES = {
    paint(id) {
      const sofa = c => `<rect x="70" y="300" width="300" height="70" rx="18" fill="${c}"/><rect x="50" y="320" width="50" height="70" rx="14" fill="${c}"/><rect x="340" y="320" width="50" height="70" rx="14" fill="${c}"/><rect x="90" y="270" width="260" height="60" rx="16" fill="${c}" opacity=".85"/><rect x="80" y="388" width="10" height="14" fill="#222"/><rect x="350" y="388" width="10" height="14" fill="#222"/>`;
      const before = `<rect width="800" height="400" fill="#B9AF98"/>
        <rect x="160" y="40" width="200" height="120" fill="#A79D86" opacity=".7" transform="rotate(-3 260 100)"/><rect x="640" y="250" width="140" height="90" fill="#C6BCA4" opacity=".7"/><rect x="40" y="130" width="100" height="140" fill="#A79D86" opacity=".6"/>
        ${scuffs(3, 9, 30, 760, 180, 370)}${crack(420, 40)}
        ${windowEl(id, 470, 80, 220, 200, '#CFC6B2', true)}
        <circle cx="500" cy="98" r="6" fill="#8A7F68"/><circle cx="660" cy="270" r="5" fill="#8A7F68"/>
        <rect y="382" width="800" height="20" fill="#C8BFAA"/>${scuffs(8, 5, 0, 780, 386, 398, '#4A4236')}
        ${floor('#7C6650', '#6A5642')}${sofa('#6B5B4B')}<rect x="420" y="402" width="70" height="40" rx="6" fill="#5D7FB0" opacity=".7"/>`;
      const after = `<rect width="800" height="400" fill="#D3E1F6"/><rect width="420" height="400" fill="#2068E8"/>
        <rect x="150" y="70" width="140" height="100" rx="4" fill="#fff"/><rect x="160" y="80" width="120" height="80" fill="#06132E"/><path d="M160 130 C200 100 240 140 280 110 V140 C240 160 200 130 160 150Z" fill="#4EF0B8" opacity=".9"/>
        ${windowEl(id, 470, 80, 220, 200, '#FFFFFF', false)}
        <rect y="382" width="800" height="20" fill="#FFFFFF"/>
        ${floor('#94775A', '#7F6449', true)}${sofa('#0F2D66')}${plant(740, 400)}
        ${sparkle(420, 300, 1.2)}${sparkle(700, 330, .8)}`;
      return [before, after, skyDefs(id)];
    },
    drywall(id) {
      const before = `<rect width="800" height="400" fill="#DCD4C4"/>
        ${hole(520, 230, 2.6)}${hole(220, 150, 1.4)}${hole(300, 300, 1)}${crack(80, 30)}${crack(620, 60)}
        <ellipse cx="420" cy="110" rx="46" ry="26" fill="#F1ECE2"/><ellipse cx="660" cy="300" rx="30" ry="22" fill="#F1ECE2"/>
        ${scuffs(12, 10, 30, 760, 240, 380)}
        <rect x="380" y="260" width="26" height="40" rx="3" fill="#EDE7DB" stroke="#9A907D" stroke-width="2" transform="rotate(8 393 280)"/>
        <rect y="382" width="800" height="20" fill="#C9C0AE"/><rect x="560" y="378" width="120" height="24" fill="#B3A991" transform="rotate(-4 620 390)"/>
        ${floor('#A89272', '#927C5E')}<path d="M500 404 l40 6 -30 10z M300 410 l20 4 -14 8z" fill="#E9E3D6"/>`;
      const after = `<rect width="800" height="400" fill="#E4ECF8"/>
        <rect x="430" y="90" width="190" height="130" rx="4" fill="#0F2D66"/><rect x="442" y="102" width="166" height="106" fill="#5B9BFF"/><path d="M442 170 l40 -36 30 26 26 -18 70 52 v14 h-166z" fill="#0F2D66"/><circle cx="580" cy="128" r="12" fill="#4EF0B8"/>
        <rect x="380" y="260" width="26" height="40" rx="3" fill="#fff" stroke="#B8C6DC" stroke-width="2"/><circle cx="393" cy="273" r="3" fill="#8DA0BE"/><circle cx="393" cy="287" r="3" fill="#8DA0BE"/>
        <rect y="382" width="800" height="20" fill="#FFFFFF"/>${floor('#B39A78', '#9D8564', true)}${plant(120, 400)}${sparkle(520, 250, 1)}${sparkle(250, 200, .7)}`;
      return [before, after, ''];
    },
    maint(id) {
      const before = `<rect width="800" height="400" fill="#BDB6A6"/>${scuffs(5, 12, 40, 760, 220, 380)}
        <rect x="290" y="80" width="200" height="320" fill="#D5CDBB"/>
        <g transform="rotate(2.4 390 240)"><rect x="305" y="95" width="170" height="305" fill="#8A6B4E"/><rect x="325" y="120" width="130" height="110" fill="#7A5D42"/><rect x="325" y="250" width="130" height="120" fill="#7A5D42"/>${scuffs(6, 5, 310, 440, 300, 390, '#3D2E20')}</g>
        <rect x="468" y="232" width="20" height="8" rx="3" fill="#8F8F86" transform="rotate(35 478 236)"/>
        <rect x="270" y="80" width="18" height="250" fill="#E4DDCC" transform="rotate(-9 279 80)"/>
        ${hole(560, 245, 1.5)}${crack(640, 120)}
        <rect x="620" y="150" width="30" height="8" fill="#6B6458" transform="rotate(20 635 154)"/>
        <rect y="382" width="800" height="20" fill="#A39C8D"/>${floor('#6E6556', '#5C5446')}<path d="M330 402 h120 l-10 18 h-100z" fill="#8F8578" opacity=".7"/>`;
      const after = `<rect width="800" height="400" fill="#E6EDF7"/>
        <rect x="290" y="80" width="200" height="320" fill="#FFFFFF"/><rect x="305" y="95" width="170" height="305" fill="#2068E8"/><rect x="325" y="120" width="130" height="110" fill="#1A57C8"/><rect x="325" y="250" width="130" height="120" fill="#1A57C8"/>
        <rect x="448" y="232" width="22" height="9" rx="4" fill="#E2B656"/><circle cx="452" cy="250" r="5" fill="#E2B656"/>
        <rect x="560" y="140" width="150" height="10" rx="5" fill="#0F2D66"/>${[585, 635, 685].map(x => `<rect x="${x - 4}" y="146" width="8" height="18" rx="3" fill="#0F2D66"/>`).join('')}
        <path d="M570 162 h40 l10 120 h-60z" fill="#C3262E"/><path d="M570 162 h40 l-6 20 h-28z" fill="#9E1E25"/><path d="M660 162 h40 l8 90 h-56z" fill="#127A62"/>
        <rect y="382" width="800" height="20" fill="#FFFFFF"/>${floor('#8C7A64', '#77664F', true)}<rect x="320" y="404" width="140" height="22" rx="6" fill="#0F2D66"/>
        <path d="M600 380 h28 v-40 h14 v40 h6 v22 h-48z M650 380 h28 v-40 h14 v40 h6 v22 h-48z" fill="#06132E"/>${plant(150, 400)}${sparkle(500, 180, .9)}`;
      return [before, after, ''];
    },
    turnover(id) {
      const before = `<rect width="800" height="400" fill="#C2BAA6"/>${scuffs(15, 12, 30, 760, 160, 380)}
        ${windowEl(id, 90, 70, 230, 210, '#CFC6B2', true)}${[110, 160, 210, 260].map((y, i) => `<path d="M100 ${y} L310 ${y + (i % 2 ? 18 : -6)}" stroke="#B5AC98" stroke-width="10"/>`).join('')}
        ${[[430, 90], [470, 140], [610, 80], [700, 150], [560, 200]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4" fill="#4A4236"/>`).join('')}
        <ellipse cx="640" cy="260" rx="70" ry="40" fill="#8F7F5E" opacity=".45"/>${hole(470, 300, 1.2)}
        <rect y="382" width="800" height="20" fill="#B3AA94"/>${floor('#7F6B55', '#6A5844')}
        <rect x="480" y="330" width="110" height="80" fill="#B88A55"/><rect x="480" y="330" width="110" height="14" fill="#A57A48"/><rect x="530" y="330" width="10" height="80" fill="#D9C08C"/>
        <rect x="590" y="350" width="80" height="60" fill="#C99A62" transform="rotate(6 630 380)"/>
        <path d="M700 410 c-30 0 -40 -60 -10 -80 c10 -8 30 -8 40 0 c30 20 20 80 -10 80z" fill="#1B1E24"/><path d="M700 330 l-8 -12 16 0z" fill="#1B1E24"/>
        ${[[200, 440], [260, 470], [380, 450], [150, 480]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="26" ry="8" fill="#5A4A38" opacity=".6"/>`).join('')}`;
      const after = `<rect width="800" height="400" fill="#E3EBF7"/>
        ${windowEl(id, 90, 70, 230, 210, '#FFFFFF', false)}
        <rect x="470" y="110" width="220" height="140" rx="4" fill="#fff"/><rect x="482" y="122" width="196" height="116" fill="#DDF8EE"/><path d="M482 200 C540 150 600 220 678 170 V238 H482Z" fill="#127A62" opacity=".8"/>
        <rect y="382" width="800" height="20" fill="#FFFFFF"/>${floor('#9A8064', '#846B51', true)}
        <rect x="420" y="410" width="160" height="26" rx="6" fill="#4EF0B8"/><text x="500" y="429" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="13" fill="#03251B">WELCOME HOME</text>
        ${plant(720, 400)}${sparkle(350, 330, 1.1)}${sparkle(620, 300, .8)}${sparkle(200, 420, .7, '#fff')}`;
      return [before, after, skyDefs(id)];
    },
    clean(id) {
      const kitchen = (cab, counter, back, handle) => `<rect width="800" height="400" fill="${back}"/>
        ${[0, 1, 2, 3].map(i => `<rect x="${60 + i * 175}" y="30" width="160" height="140" rx="6" fill="${cab}"/><rect x="${126 + i * 175}" y="140" width="28" height="6" rx="3" fill="${handle}"/>`).join('')}
        ${[0, 1, 2, 3].map(i => `<rect x="${60 + i * 175}" y="270" width="160" height="125" rx="6" fill="${cab}"/><rect x="${126 + i * 175}" y="284" width="28" height="6" rx="3" fill="${handle}"/>`).join('')}
        <rect x="40" y="250" width="720" height="22" rx="4" fill="${counter}"/><rect x="330" y="252" width="150" height="12" rx="4" fill="#9AA6B8"/><path d="M400 252 v-42 q0 -14 14 -14 h18 v8" stroke="#8D99AD" stroke-width="7" fill="none" stroke-linecap="round"/>`;
      const r = rng(41); let crumbs = ''; for (let i = 0; i < 40; i++) crumbs += `<circle cx="${(60 + r() * 680).toFixed(0)}" cy="${(254 + r() * 10).toFixed(0)}" r="${(1 + r() * 2).toFixed(1)}" fill="#6B4E2E"/>`;
      const before = kitchen('#CFC8B6', '#9F9682', '#D8D0BC', '#6E6656') +
        `<rect width="800" height="400" fill="#7A6440" opacity=".14"/>
        ${[[120, 200, 30], [260, 220, 18], [560, 205, 26], [690, 225, 16]].map(([x, y, s]) => `<ellipse cx="${x}" cy="${y}" rx="${s}" ry="${s * .6}" fill="#8A6A35" opacity=".45"/>`).join('')}
        ${[[160, 258, 40], [600, 258, 30]].map(([x, y, s]) => `<ellipse cx="${x}" cy="${y}" rx="${s}" ry="5" fill="#5A3E1E" opacity=".5"/>`).join('')}${crumbs}
        <g><rect x="500" y="214" width="70" height="10" rx="4" fill="#EDE9DF"/><rect x="505" y="204" width="60" height="10" rx="4" fill="#E4DFD2"/><rect x="510" y="194" width="50" height="10" rx="4" fill="#EDE9DF"/><rect x="515" y="232" width="40" height="18" rx="3" fill="#C9C1AC"/></g>
        <rect x="235" y="30" width="160" height="140" rx="6" fill="#BFB7A3" transform="rotate(-12 235 100)"/>
        ${floor('#8E8676', '#787061')}${[[300, 440], [520, 470]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="40" ry="10" fill="#5A4A38" opacity=".4"/>`).join('')}`;
      const after = kitchen('#FFFFFF', '#0F2D66', '#E8F0FB', '#2068E8') +
        `<path d="M40 252 h720 v6 h-720z" fill="#5B9BFF" opacity=".6"/>
        <circle cx="600" cy="236" r="16" fill="#0F2D66"/><circle cx="594" cy="228" r="8" fill="#E2B656"/><circle cx="606" cy="230" r="8" fill="#E2B656"/>
        ${floor('#C9D3E2', '#B3BFD1', true)}${sparkle(150, 210, 1.3)}${sparkle(470, 190, 1)}${sparkle(700, 210, .8)}${sparkle(280, 330, .9, '#5B9BFF')}`;
      return [before, after, ''];
    },
    commercial(id) {
      const desk = (top, front) => `<rect x="220" y="290" width="360" height="22" rx="4" fill="${top}"/><rect x="236" y="312" width="328" height="90" fill="${front}"/>`;
      const before = `<rect width="800" height="400" fill="#A9AAA3"/>${scuffs(21, 14, 30, 760, 160, 380, '#4A4A44')}
        <path d="M80 80 l60 -10 10 50 -50 30z M640 120 l70 10 -10 60 -60 -20z" fill="#C9CAC2"/>
        <rect x="270" y="90" width="260" height="60" rx="6" fill="#7E7F78"/><text x="400" y="131" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="30" fill="#C7C8C0" letter-spacing="4">REC PT ON</text>
        ${desk('#8D8676', '#7B7466')}${scuffs(22, 6, 240, 560, 320, 390, '#3D3A33')}
        <rect y="382" width="800" height="20" fill="#8F908A"/>${floor('#6D6E69', '#5D5E59')}
        <path d="M640 330 h70 v70 h-10 v-40 h-50 v40 h-10z" fill="#5E4C3A"/><path d="M650 290 h50 v40 h-50z" fill="#6D5A46" transform="rotate(-8 675 310)"/>`;
      const after = `<rect width="800" height="400" fill="#0F2D66"/><rect x="560" width="240" height="400" fill="#E6EDF7"/>
        <text x="300" y="138" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="900" font-size="46" fill="#4EF0B8" letter-spacing="6">WELCOME</text>
        ${[300, 470].map(x => `<path d="M${x} 0 v40" stroke="#E2B656" stroke-width="3"/><path d="M${x - 26} 64 q26 -34 52 0z" fill="#E2B656"/>`).join('')}
        ${desk('#FFFFFF', '#2068E8')}<rect x="236" y="312" width="328" height="10" fill="#4EF0B8"/>
        <rect y="382" width="800" height="20" fill="#FFFFFF"/>${floor('#B7C4D8', '#A1B0C7', true)}${plant(680, 400)}${sparkle(150, 220, 1.1)}${sparkle(520, 200, .8)}`;
      return [before, after, ''];
    },
    seasonal(id) {
      const scene = (lawn, siding) => `<rect width="800" height="500" fill="#BFD8F2"/><circle cx="680" cy="70" r="34" fill="#FFE7A3"/>
        <rect x="200" y="110" width="400" height="270" fill="${siding}"/>${[140, 170, 200, 230, 260, 290, 320, 350].map(y => `<path d="M200 ${y}H600" stroke="#000" stroke-opacity=".08" stroke-width="2"/>`).join('')}
        <path d="M180 120 L400 20 L620 120Z" fill="#0F2D66"/><rect x="350" y="230" width="100" height="150" fill="#06132E"/><circle cx="435" cy="310" r="5" fill="#E2B656"/>
        ${windowEl(id, 240, 180, 80, 80, '#fff', false)}${windowEl(id, 480, 180, 80, 80, '#fff', false)}
        <rect y="380" width="800" height="120" fill="${lawn}"/><rect x="330" y="380" width="140" height="18" fill="#9AA6B8"/><path d="M350 398 h100 l80 102 h-260z" fill="#B8C2D0"/>`;
      const r = rng(55); let leaves = ''; for (let i = 0; i < 120; i++) { const x = r() * 800, y = 385 + r() * 112; leaves += `<ellipse cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" rx="${(5 + r() * 5).toFixed(1)}" ry="${(2.5 + r() * 2).toFixed(1)}" fill="${['#D9822B', '#B85C2C', '#E2B656', '#8A5A2B'][i % 4]}" transform="rotate(${(r() * 180).toFixed(0)} ${x.toFixed(0)} ${y.toFixed(0)})"/>`; }
      const shrubs = (c, wild) => [120, 680].map(x => wild ? `<path d="M${x - 70} 390 q-10 -70 30 -90 q20 -40 60 -10 q40 -20 50 30 q30 30 0 70z" fill="${c}"/>` : `<ellipse cx="${x}" cy="360" rx="60" ry="36" fill="${c}"/>`).join('');
      const before = scene('#8A9A5B', '#9C8C78') + shrubs('#5A6B35', true) + leaves +
        `<path d="M520 450 l60 -30 M540 440 l14 -22 M300 470 l-50 -20" stroke="#5C4630" stroke-width="5" stroke-linecap="round"/><path d="M200 380 q40 -20 90 0z" fill="#E8EEF5" opacity=".7"/>`;
      const after = scene('#4E9A5F', '#5B9BFF') + shrubs('#2F7A47', false) +
        `<path d="M350 398 h100 l80 102 h-260z" fill="#D6DEEA"/>${sparkle(400, 440, 1.1)}${sparkle(140, 300, .8)}${sparkle(650, 300, .8)}`;
      return [before, after, skyDefs(id)];
    },
    junk(id) {
      const garage = (wall, fl) => `<rect width="800" height="400" fill="${wall}"/>${[100, 200, 300].map(y => `<path d="M0 ${y}H800" stroke="#000" stroke-opacity=".06" stroke-width="3"/>`).join('')}<rect y="400" width="800" height="100" fill="${fl}"/><path d="M0 400 H800" stroke="#000" stroke-opacity=".15" stroke-width="3"/>`;
      const box = (x, y, w, h, c = '#B88A55') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/><rect x="${x}" y="${y}" width="${w}" height="10" fill="#000" opacity=".1"/><rect x="${x + w / 2 - 6}" y="${y}" width="12" height="${h}" fill="#E6D3A8" opacity=".8"/>`;
      const before = garage('#B8B9B4', '#8F908B') +
        box(40, 250, 140, 150) + box(60, 150, 110, 100, '#C99A62') + box(190, 300, 120, 100, '#A57A48') + box(200, 220, 90, 80) +
        `<path d="M330 400 v-90 h110 v-60 h20 v150 h-20 v-40 h-90 v40z" fill="#5E4C3A"/><rect x="340" y="300" width="100" height="30" rx="8" fill="#7A6450"/>
        <circle cx="530" cy="360" r="42" fill="#1B1E24"/><circle cx="530" cy="360" r="20" fill="#8F908B"/>
        <path d="M600 410 c-40 0 -50 -70 -14 -92 c14 -10 40 -10 54 0 c36 22 26 92 -14 92z" fill="#1B1E24"/><path d="M680 410 c-30 0 -40 -50 -10 -66 c10 -8 30 -8 40 0 c26 16 20 66 -10 66z" fill="#2A2E36"/>
        ${box(640, 200, 120, 120, '#C99A62')}<path d="M90 420 l60 20 M420 440 l40 -10" stroke="#5C5D58" stroke-width="6" stroke-linecap="round"/>
        ${[[300, 460], [500, 450], [700, 470]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="34" ry="8" fill="#5E5F5A" opacity=".5"/>`).join('')}`;
      const after = garage('#E4EAF2', '#B9C2CF') +
        `<rect x="80" y="80" width="300" height="180" rx="6" fill="#C9D3E2"/>${Array.from({ length: 6 }, (_, i) => Array.from({ length: 10 }, (_, j) => `<circle cx="${100 + j * 29}" cy="${100 + i * 28}" r="2.4" fill="#9DAAC0"/>`).join('')).join('')}
        <path d="M140 120 v70 M130 120 h20" stroke="#0F2D66" stroke-width="6" stroke-linecap="round"/><path d="M220 110 l30 90" stroke="#C3262E" stroke-width="7" stroke-linecap="round"/><circle cx="310" cy="160" r="22" fill="none" stroke="#2068E8" stroke-width="6"/>
        <rect x="500" y="120" width="240" height="12" fill="#0F2D66"/><rect x="500" y="250" width="240" height="12" fill="#0F2D66"/><rect x="500" y="120" width="10" height="280" fill="#0F2D66"/><rect x="730" y="120" width="10" height="280" fill="#0F2D66"/>
        <rect x="520" y="190" width="90" height="60" rx="6" fill="#4EF0B8"/><rect x="625" y="190" width="90" height="60" rx="6" fill="#5B9BFF"/><rect x="540" y="320" width="160" height="80" rx="6" fill="#2068E8"/>
        <path d="M60 470 L420 470 L380 430 L100 430Z" fill="#fff" opacity=".18"/>${sparkle(300, 410, 1.2)}${sparkle(450, 300, .8)}`;
      return [before, after, ''];
    }
  };
  $$('.ba[data-scene]').forEach(ba => {
    const fn = SCENES[ba.dataset.scene];
    if (!fn || ba.querySelector('img')) return;
    const id = ++uid;
    const [b, a, defs] = fn(id);
    ba.insertAdjacentHTML('afterbegin', svgWrap('before', b, defs) + svgWrap('after', a, defs));
  });
  $$('.ba').forEach(ba => {
    const input = ba.querySelector('input');
    if (!input) return;
    const set = v => ba.style.setProperty('--pos', v + '%');
    input.addEventListener('input', () => set(input.value));
    set(input.value);
  });

  /* ==========================================================
     Project estimator
     ========================================================== */
  const est = $('#estimator');
  if (est) {
    const SERV = {
      painting: { label: 'Interior painting', quote: 'Painting & finishing', scope: ['Surface prep & patching', 'Walls and ceilings', 'Trim, doors & baseboards', 'Cleanup & final check'], turn: ['Typically 1–2 days on site', 'Typically 2–4 days on site', 'Typically 4–7 days on site', 'Typically 1–2 weeks, can be phased'], w: 0 },
      reset: { label: 'Full rental reset', quote: 'Rental turnover / YK Rental Reset', scope: ['Unit inspection & photos', 'Painting & drywall repair', 'Cleaning & garbage removal', 'Final walkthrough'], turn: ['Typically 2–3 days', 'Typically 1–2 weeks, can be phased', 'Typically 1–2 weeks, can be phased', 'Typically 2+ weeks, phased unit by unit'], w: 2 },
      repairs: { label: 'Handyman & repairs', quote: 'Drywall & repairs', scope: ['Walkthrough of your repair list', 'Drywall, doors, trim & hardware', 'Caulking, sealing & fixture work', 'Cleanup & sign-off'], turn: ['Typically a half to full day', 'Typically 1–2 days', 'Typically 2–4 days', 'Scheduled visits, can be recurring'], w: 0 },
      cleaning: { label: 'Deep cleaning', quote: 'Cleaning', scope: ['Kitchen & appliances', 'Bathrooms sanitized', 'Floors, baseboards & surfaces', 'Final walkthrough'], turn: ['Typically a few hours', 'Typically 1 day', 'Typically 1–2 days', 'Typically 2+ days or scheduled by area'], w: 0 },
      seasonal: { label: 'Seasonal prep', quote: 'Seasonal services', scope: ['Property walkaround & checklist', 'Snow, yard or debris clearing', 'Weather stripping & draft sealing', 'Exterior touch-ups'], turn: ['Typically a same-day visit', 'Typically 1 day', 'Typically 1–2 days', 'Recurring seasonal schedule'], w: 0 },
      junk: { label: 'Junk removal', quote: 'Junk removal', scope: ['Sort what to haul, donate or recycle', 'Loading & haul-away', 'Responsible disposal', 'Sweep-out of the cleared space'], turn: ['Typically a single visit', 'Typically a half day', 'Typically 1 day', 'Typically 1–2 days, can be phased'], w: 0 }
    };
    const PROP_TO_FORM = { 'Single-family home': 'Home', 'Rental unit / apartment': 'Rental unit / apartment', 'Multi-unit building': 'Multi-unit building', 'Commercial space': 'Commercial' };
    const TIERS = ['Standard Project', 'Standard Project', 'Full Project', 'Large Project', 'Multi-phase Project', 'Multi-phase Project', 'Multi-phase Project'];
    const panes = $$('.est-pane', est);
    const stepsUI = $$('.est-steps li', est);
    const bar = $('.est-bar i', est);
    let step = 0;
    const val = name => { const c = $(`input[name="${name}"]:checked`, est); return c ? c.value : null; };
    function show(i) {
      step = i;
      panes.forEach((p, k) => p.classList.toggle('on', k === i));
      stepsUI.forEach((li, k) => { li.classList.toggle('on', k === i); li.classList.toggle('done', k < i); });
      bar.style.width = ((i + 1) / panes.length * 100) + '%';
      update();
      if (i === 3) summary();
    }
    function update() {
      const need = ['eProp', 'eServ', 'eSize'][step];
      const next = $('.est-pane.on [data-next]', est);
      if (next) next.disabled = need ? !val(need) : false;
    }
    function summary() {
      const p = val('eProp'), sKey = val('eServ'), z = val('eSize');
      const s = SERV[sKey];
      const sizes = $$('input[name="eSize"]', est).map(i => i.value);
      const zi = sizes.indexOf(z);
      const extras = $$('input[name="eExtra"]:checked', est).map(i => i.value);
      const score = zi + s.w + (extras.length >= 2 ? 1 : 0);
      $('#eTier').textContent = TIERS[Math.min(score, TIERS.length - 1)];
      $('#eWhat').textContent = `${s.label} · ${p} · ${z}`;
      $('#eTurn').textContent = s.turn[zi];
      $('#eScope').innerHTML = s.scope.concat(extras).map(t => `<li>${t}</li>`).join('');
      const details = `Estimator summary: ${s.label} for a ${p.toLowerCase()} (${z}).` + (extras.length ? ` Also: ${extras.join(', ')}.` : '') + '\n\nMore details: ';
      const q = new URLSearchParams({ service: s.quote, property: PROP_TO_FORM[p] || '', details });
      $('#eQuote').href = 'get-a-quote.html?' + q.toString() + '#quote';
    }
    est.addEventListener('change', update);
    est.addEventListener('click', e => {
      const t = e.target.closest('[data-next],[data-back],[data-reset]');
      if (!t) return;
      if (t.hasAttribute('data-next')) show(Math.min(step + 1, panes.length - 1));
      if (t.hasAttribute('data-back')) show(Math.max(step - 1, 0));
      if (t.hasAttribute('data-reset')) { $$('input', est).forEach(i => { i.checked = false; }); show(0); }
    });
    // Auto-advance after a single-choice pick (not on the size step, which has extras)
    est.addEventListener('change', e => {
      if (e.target.type === 'radio' && (e.target.name === 'eProp' || e.target.name === 'eServ')) setTimeout(() => show(step + 1), 220);
    });
    show(0);
  }

  /* ==========================================================
     Quote form
     - Main button submits to FormSubmit (emails the team, supports a photo)
     - WhatsApp / email buttons build a ready-to-send message instead
     ========================================================== */
  const form = $('#quoteForm');
  if (form) {
    const err = $('#formError');
    const params = new URLSearchParams(location.search);
    const setSel = (name, v) => { const el = form.elements[name]; if (el && v && [...el.options].some(o => o.value === v)) el.value = v; };
    setSel('service', params.get('service'));
    setSel('property_type', params.get('property'));
    if (params.get('details') && form.elements.details) form.elements.details.value = params.get('details');

    const fileIn = form.elements.attachment;
    const fileList = $('#fileList');
    const drop = $('.file-drop', form);
    const MAX = 5 * 1024 * 1024;
    if (fileIn) {
      fileIn.addEventListener('change', () => {
        const f = fileIn.files[0];
        if (f && f.size > MAX) { err.textContent = 'That photo is over 5 MB. Choose a smaller one, or send it by WhatsApp.'; fileIn.value = ''; fileList.textContent = ''; return; }
        err.textContent = '';
        fileList.textContent = f ? '✓ ' + f.name : '';
      });
      ['dragenter', 'dragover'].forEach(ev => drop.addEventListener(ev, () => drop.classList.add('drag')));
      ['dragleave', 'drop'].forEach(ev => drop.addEventListener(ev, () => drop.classList.remove('drag')));
    }
    const LABELS = { name: 'your name', phone: 'a phone number', details: 'a project description' };
    function collect() {
      const f = new FormData(form);
      const d = {};
      for (const [k, v] of f.entries()) if (typeof v === 'string') d[k] = v.trim();
      const missing = [];
      ['name', 'phone', 'details'].forEach(k => {
        const el = form.elements[k];
        const bad = !d[k];
        el.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) missing.push(k);
      });
      const em = form.elements.email;
      if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) { em.setAttribute('aria-invalid', 'true'); missing.push('email'); }
      if (missing.length) {
        err.textContent = missing.includes('email') && missing.length === 1 ? 'Check the email address.' : 'Add ' + missing.filter(m => m !== 'email').map(k => LABELS[k]).join(', ').replace(/, ([^,]*)$/, ' and $1') + ' to send the request.';
        form.elements[missing[0]].focus();
        return null;
      }
      err.textContent = '';
      const lines = ["Hi YK Property Services, I'd like a free quote.", '', 'Name: ' + d.name, 'Phone: ' + d.phone];
      if (d.email) lines.push('Email: ' + d.email);
      if (d.address) lines.push('Property address: ' + d.address);
      lines.push('Property type: ' + d.property_type, 'Service: ' + d.service);
      if (d.date) lines.push('Preferred date: ' + d.date);
      lines.push('Preferred contact: ' + d.contact_method, '', d.details);
      return { d, msg: lines.join('\n') };
    }
    form.addEventListener('submit', e => {
      const r = collect();
      if (!r) { e.preventDefault(); return; }
      const next = form.elements._next;
      if (next) next.value = new URL('thanks.html', location.href).href;
      const subj = form.elements._subject;
      if (subj) subj.value = `New quote request: ${r.d.service} — ${r.d.name}`;
      const btn = $('button[type="submit"]', form);
      btn.disabled = true; btn.lastChild.textContent = ' Sending…';
    });
    $('#waBtn').addEventListener('click', () => { const r = collect(); if (r) window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(r.msg), '_blank', 'noopener'); });
    $('#emailBtn').addEventListener('click', () => { const r = collect(); if (r) location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Quote request: ' + r.d.service) + '&body=' + encodeURIComponent(r.msg); });
    form.addEventListener('input', e => { if (e.target.getAttribute('aria-invalid') === 'true' && e.target.value.trim()) { e.target.setAttribute('aria-invalid', 'false'); err.textContent = ''; } });
  }

  /* ---------- Reviews ---------- */
  $$('[data-reviews]').forEach(box => {
    const cat = box.dataset.reviews;
    const list = REVIEWS.filter(r => !cat || !r.cat || r.cat === cat);
    if (!list.length) return;
    box.innerHTML = list.slice(0, 3).map(r => `<figure class="rv"><blockquote>“${r.text}”</blockquote><cite>${r.name}<small>${r.detail || ''}</small></cite></figure>`).join('');
    const score = box.closest('.reviews') && box.closest('.reviews').querySelector('.rv-score strong');
    if (score) score.textContent = list.length + (list.length === 1 ? ' verified review' : ' verified reviews');
  });

  /* ==========================================================
     YK Assistant — quick answers from a fixed list, no AI, no tracking
     ========================================================== */
  const assist = $('#assist');
  if (assist) {
    const log = $('.assist-log', assist);
    const input = $('#assistInput');
    const Q = 'get-a-quote.html#quote';
    const KB = [
      { k: ['turnover', 'rental reset', 'tenant', 'move-out', 'move out', 'between tenants', 'vacant'], a: `<p><strong>YK Rental Reset</strong> gets a unit from move-out to move-in ready with one call:</p><ul><li>Unit inspection and photos</li><li>Drywall patching and painting</li><li>Cleaning and garbage removal</li><li>Minor repairs, hardware and fixture checks</li><li>Final walkthrough with photo documentation</li></ul><p>Tell us the move-out date and unit size and we'll schedule it. <a href="rental-turnovers.html">How turnovers work →</a></p>` },
      { k: ['winter', 'cold', 'paint in', 'season to paint', 'january', 'december', 'february'], a: `<p>Yes — interior painting runs all year. Winter is actually a great time for it: we can repaint rooms, patch drywall and seal drafts while it's minus thirty outside.</p><p>Exterior painting and deck or fence staining are booked for the warmer months. <a href="painting.html">Painting services →</a></p>` },
      { k: ['landlord', 'property manager', 'portfolio', 'units', 'multiple properties', 'invoice', 'invoicing'], a: `<p>For landlords and property managers we offer:</p><ul><li>Priority scheduling</li><li>Monthly invoicing</li><li>Recurring maintenance agreements</li><li>Coordinated turnovers with photo documentation</li></ul><p>One contact instead of several contractors. <a href="rental-turnovers.html">Rental services →</a></p>` },
      { k: ['where do i start', 'few repairs', 'repair list', 'handyman', 'fix', 'repairs', 'broken'], a: `<p>Easiest way: send us your whole list, with a few photos if you can. We'll group the work so it's done in as few visits as possible, and send a clear estimate first.</p><p><a href="${Q}">Send your list →</a> or WhatsApp <a href="https://wa.me/${WA}" target="_blank" rel="noopener">(705) 500-8455</a>.</p>` },
      { k: ['price', 'cost', 'how much', 'rate', 'expensive', 'cheap', 'charge', 'estimate', 'quote'], a: `<p>Every property is different, so we give a clear written estimate before any work starts — estimates are free.</p><p>Try the <a href="index.html#estimator">project estimator</a> for scope and typical turnaround, then <a href="${Q}">request your free quote</a>.</p>` },
      { k: ['airbnb', 'short-term', 'short term', 'vrbo', 'host', 'guest', 'listing'], a: `<p>For Airbnb and VRBO hosts we do same-day turnover cleaning, linen changes, restocking (host-provided supplies), photo reports after each visit, quick fixes and winter walkway clearing.</p><p>You don't need to be in Yellowknife. <a href="airbnb-hosts.html">Host services →</a></p>` },
      { k: ['clean', 'deep clean', 'move-in', 'post-renovation', 'post-construction', 'office cleaning'], a: `<p>We do move-out, move-in, deep, turnover, post-renovation, office and common-area cleaning. <a href="cleaning.html">Cleaning services →</a></p>` },
      { k: ['snow', 'shovel', 'yard', 'leaves', 'spring', 'fall', 'seasonal', 'pressure wash', 'stain'], a: `<p>Seasonal work includes snow clearing for walkways and entrances, spring and fall yard cleanup, deck and fence staining, pressure washing, weather stripping and seasonal property checks. <a href="seasonal-services.html">Seasonal services →</a></p>` },
      { k: ['junk', 'haul', 'garbage', 'removal', 'cleanout', 'clean out', 'dispose', 'dump'], a: `<p>We clear out garages, basements, estates and rentals, haul it away and dispose of it responsibly — donation sorting included. <a href="junk-removal.html">Junk removal →</a></p>` },
      { k: ['commercial', 'office', 'business', 'retail', 'restaurant', 'warehouse', 'store'], a: `<p>Yes — commercial painting, repairs, cleaning, common-area maintenance and scheduled service contracts for offices, retail, restaurants and buildings, with monthly invoicing available. <a href="commercial-services.html">Commercial services →</a></p>` },
      { k: ['drywall', 'hole', 'crack', 'patch', 'caulk', 'door', 'trim', 'baseboard'], a: `<p>We patch holes and cracks, blend texture, caulk and seal, adjust doors and hardware, and repair trim and baseboards — then paint so it looks like the damage never happened. <a href="drywall-repairs.html">Drywall & repairs →</a></p>` },
      { k: ['floor', 'laminate', 'vinyl', 'tile', 'light fixture', 'fixture', 'light'], a: `<p>Yes — we install and repair laminate, vinyl and tile flooring, and swap out light fixtures. Send photos and measurements for a faster quote. <a href="${Q}">Request a quote →</a></p>` },
      { k: ['cabin', 'cottage'], a: `<p>We help with cabins too: opening up in spring, closing down in fall, cleaning, painting and repairs in between. <a href="${Q}">Tell us about your cabin →</a></p>` },
      { k: ['hour', 'open', 'sunday', 'saturday', 'weekend', 'when are you'], a: `<p>We're available <strong>Monday to Saturday, 8:00 AM – 6:00 PM</strong>, closed Sundays. You can send a quote request or email any time.</p>` },
      { k: ['area', 'where', 'location', 'serve', 'service area', 'outside', 'near'], a: `<p>We serve Yellowknife and the surrounding area. Send your property location and we'll confirm availability. <a href="service-areas.html">Service area →</a></p>` },
      { k: ['photo', 'picture', 'image', 'upload'], a: `<p>Yes, please! Add a photo to the <a href="${Q}">quote form</a>, or send as many as you like on WhatsApp at <a href="https://wa.me/${WA}" target="_blank" rel="noopener">(705) 500-8455</a>.</p>` },
      { k: ['recurring', 'regular', 'monthly', 'weekly', 'contract', 'ongoing', 'plan'], a: `<p>Recurring maintenance and cleaning plans are available for homes, landlords, property managers and commercial properties. Mention how often you need us in your <a href="${Q}">quote request</a>.</p>` },
      { k: ['phone', 'call', 'contact', 'email', 'whatsapp', 'text', 'reach'], a: `<p>Call or text <a href="tel:${PHONE}">+1 (705) 500-8455</a> or <a href="tel:+16475400097">+1 (647) 540-0097</a>, WhatsApp <a href="https://wa.me/${WA}" target="_blank" rel="noopener">(705) 500-8455</a>, or email <a href="mailto:${EMAIL}">${EMAIL}</a>.</p>` },
      { k: ['hello', 'hi', 'hey', 'good morning', 'good afternoon'], a: `<p>Hi! Ask me about painting, repairs, cleaning, rental turnovers, seasonal work or commercial service.</p>` },
      { k: ['thank', 'thanks', 'great', 'perfect'], a: `<p>You're welcome! When you're ready, <a href="${Q}">request a free quote</a> and the team will follow up.</p>` }
    ];
    const FALLBACK = `<p>I'm a simple assistant, so I may not have that answer. The team can help directly:</p><p>Call <a href="tel:${PHONE}">+1 (705) 500-8455</a>, WhatsApp <a href="https://wa.me/${WA}" target="_blank" rel="noopener">us</a>, or <a href="${Q}">send a quote request</a>.</p>`;
    const esc = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    function answer(q) {
      const t = ' ' + q.toLowerCase() + ' ';
      let best = null, bestScore = 0;
      KB.forEach(item => {
        let s = 0;
        item.k.forEach(k => { if (t.includes(k)) s += k.length > 5 ? 2 : 1; });
        if (s > bestScore) { bestScore = s; best = item; }
      });
      return best ? best.a : FALLBACK;
    }
    const add = (html, who) => { const m = document.createElement('div'); m.className = 'msg ' + who; m.innerHTML = html; log.appendChild(m); log.scrollTop = log.scrollHeight; return m; };
    const intro = log.innerHTML;
    function ask(q) {
      if (!q.trim()) return;
      add(esc(q), 'me');
      const typing = add('<p>…</p>', 'bot');
      setTimeout(() => { typing.innerHTML = answer(q); log.scrollTop = log.scrollHeight; }, 450);
    }
    const setOpen = open => {
      document.body.classList.toggle('assist-open', open);
      $('#assistBtn').setAttribute('aria-expanded', open);
      if (open) setTimeout(() => input.focus(), 250);
    };
    $('#assistBtn').addEventListener('click', () => setOpen(true));
    $('.x', assist).addEventListener('click', () => { setOpen(false); $('#assistBtn').focus(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && document.body.classList.contains('assist-open')) setOpen(false); });
    log.addEventListener('click', e => { const b = e.target.closest('.sugg button'); if (b) ask(b.textContent); });
    $('#assistForm').addEventListener('submit', e => { e.preventDefault(); ask(input.value); input.value = ''; });
    $('#assistClear').addEventListener('click', () => { log.innerHTML = intro; input.focus(); });
  }
})();
