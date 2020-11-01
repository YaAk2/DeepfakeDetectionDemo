const face = ".tanuki-shape";
const ear = ".tanuki-shapes";
const hoverColor = 'rgba(252, 163, 38, 0.42)';
var tl = new TimelineMax({
  repeat: -1,
  repeatDelay: .3,
  
  yoyo: true
});

tl.set(face, {
  scale: 0,
  opacity: 0,
  transformOrigin: "top bottom"
});
tl.set(ear, {
  
  y:30,
  opacity:0,
  scale:0,
});
tl.staggerTo(face, 1, {
  scale: 1,
  opacity: 1,
  ease: Elastic.easeInOut,
}, 0.06,0)
tl.staggerTo(ear, 1, {
  delay:0.5,
  scale: 1,
  opacity: 1,
  
  y:0,
  ease: Elastic.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-left-cheek', 0.2, {
  delay:1.5,
  fill:'#fff',
  
  ease: Ease.easeInOut,
}, 0.06,0);
tl.staggerTo('.tanuki-left-cheek', 0.2, {
  delay:1.7,
  fill:'#fca326',
  ease: Ease.easeInOut,
}, 0.06,0);
tl.staggerTo('.tanuki-left-eye', 0.2, {
  delay:1.7,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-left-ear', 0.2, {
  delay:1.7,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-left-eye', 0.2, {
  
  delay:1.9,
  fill:'#fc6d26',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-left-ear', 0.2, {
  delay:1.9,
  fill:'#e24329',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-nose', 0.2, {
  delay:1.9,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-nose', 0.2, {
  delay:2.1,
  fill:'#e24329',
  ease: Ease.easeInOut,
}, 0.06,0);
tl.staggerTo('.tanuki-right-eye', 0.2, {
  
  delay:2.1,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-right-ear', 0.2, {
  delay:2.1,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-right-eye', 0.2, {
  
  delay:2.3,
  fill:'#fc6d26',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-right-ear', 0.2, {
  delay:2.3,
  fill:'#e24329',
  ease: Ease.easeInOut,
}, 0.06,0)
tl.staggerTo('.tanuki-right-cheek', 0.2, {
  delay:2.3,
  fill:'#fff',
  ease: Ease.easeInOut,
}, 0.06,0);
tl.staggerTo('.tanuki-right-cheek', 0.2, {
  delay:2.5,
  fill:'#fca326',
  ease: Ease.easeInOut,
}, 0.06,0);