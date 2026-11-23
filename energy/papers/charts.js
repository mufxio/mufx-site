/* Small SVG chart helpers in the mufx light paper style. No dependencies. */
(function(){
var NS='http://www.w3.org/2000/svg';
var C={ink:'#191d1f',ink2:'#3f474b',ink3:'#6a7379',grid:'#d3d8d2',acc:'#14538c',band:'#dcdfda'};
function el(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e;}
function svg(host,W,H,label){var s=el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':label||''});s.style.width='100%';s.style.height='auto';s.style.display='block';host.appendChild(s);return s;}
function text(s,x,y,t,o){o=o||{};var a={x:x,y:y,'font-size':o.size||10,'text-anchor':o.anchor||'start'};a.style='fill:'+(o.color||C.ink2)+';font-family:Spline Sans Mono,ui-monospace,monospace';s.appendChild(el('text',a,t));}
function yaxis(s,L,R,W,T,ph,ymin,ymax,ticks,fmt){
  ticks.forEach(function(v){var y=T+ph-(v-ymin)/(ymax-ymin)*ph;
    s.appendChild(el('line',{x1:L,x2:W-R,y1:y,y2:y,stroke:v===0?C.ink3:C.grid,'stroke-width':v===0?0.8:0.7}));
    text(s,L-6,y+3.5,fmt?fmt(v):v,{anchor:'end'});});
}
function legend(host,items){var d=document.createElement('div');d.className='legend';
  items.forEach(function(it){var sp=document.createElement('span');var i=document.createElement('i');
    i.style.borderTop=(it.dash?'1.6px dashed ':(it.bar?'8px solid ':'2px solid '))+it.color;sp.appendChild(i);sp.appendChild(document.createTextNode(it.name));d.appendChild(sp);});
  host.appendChild(d);}

/* line chart: o = {labels, series:[{name,values,color,dash,width}], ymin,ymax,yticks,yfmt, xtickEvery|xticks:[idx], bands:[[i0,i1,label]], ytitle} */
window.mfLine=function(host,o){
  var W=640,H=o.height||280,L=48,R=12,T=24,B=30,pw=W-L-R,ph=H-T-B,n=o.labels.length;
  var s=svg(host,W,H,o.label);
  function X(i){return L+i/(n-1)*pw} function Y(v){return T+ph-(v-o.ymin)/(o.ymax-o.ymin)*ph}
  (o.bands||[]).forEach(function(b){s.appendChild(el('rect',{x:X(b[0]),y:T,width:X(b[1])-X(b[0]),height:ph,fill:C.band}));
    text(s,X(b[0])+4,T+11,b[2],{size:9,color:C.ink3});});
  yaxis(s,L,R,W,T,ph,o.ymin,o.ymax,o.yticks,o.yfmt);
  if(o.ytitle)text(s,L,T-10,o.ytitle,{size:10,color:C.ink});
  (o.xticks||[]).forEach(function(i){var x=X(i);s.appendChild(el('line',{x1:x,x2:x,y1:T+ph,y2:T+ph+3,stroke:C.ink3,'stroke-width':0.7}));
    text(s,x,T+ph+15,o.xlab?o.xlab(o.labels[i]):o.labels[i],{anchor:'middle'});});
  o.series.forEach(function(sr){var d='',pen=false;
    sr.values.forEach(function(v,i){if(v==null){pen=false;return;}d+=(pen?'L':'M')+X(i).toFixed(1)+','+Y(v).toFixed(1);pen=true;});
    var a={d:d,fill:'none',stroke:sr.color,'stroke-width':sr.width||1.6,'stroke-linejoin':'round'};if(sr.dash)a['stroke-dasharray']='4 3';s.appendChild(el('path',a));});
  legend(host,o.series);
};

/* grouped bars: o = {groups:[labels], series:[{name,values,color}], ymin,ymax,yticks,yfmt, valfmt, ytitle} */
window.mfBars=function(host,o){
  var W=640,H=o.height||260,L=48,R=12,T=24,B=30,pw=W-L-R,ph=H-T-B,g=o.groups.length,k=o.series.length;
  var s=svg(host,W,H,o.label);
  function Y(v){return T+ph-(v-o.ymin)/(o.ymax-o.ymin)*ph}
  yaxis(s,L,R,W,T,ph,o.ymin,o.ymax,o.yticks,o.yfmt);
  if(o.ytitle)text(s,L,T-10,o.ytitle,{size:10,color:C.ink});
  var gw=pw/g,bw=Math.min(34,gw*0.7/k);
  o.groups.forEach(function(lab,gi){var x0=L+gi*gw+(gw-bw*k)/2;
    o.series.forEach(function(sr,si){var v=sr.values[gi];if(v==null)return;var x=x0+si*bw,y0=Y(0),y1=Y(v);
      s.appendChild(el('rect',{x:x+1,y:Math.min(y0,y1),width:bw-2,height:Math.max(Math.abs(y1-y0),0.8),fill:sr.color}));
      if(o.valfmt)text(s,x+bw/2,(v>=0?y1-4:y1+11),o.valfmt(v),{anchor:'middle',size:9,color:C.ink});});
    text(s,L+gi*gw+gw/2,T+ph+15,lab,{anchor:'middle'});});
  if(k>1)legend(host,o.series.map(function(x){return {name:x.name,color:x.color,bar:true}}));
};
window.mfC=C;
})();
