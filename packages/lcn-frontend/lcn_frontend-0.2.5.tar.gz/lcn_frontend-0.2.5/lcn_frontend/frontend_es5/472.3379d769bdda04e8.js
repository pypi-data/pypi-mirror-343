/*! For license information please see 472.3379d769bdda04e8.js.LICENSE.txt */
"use strict";(self.webpackChunklcn_frontend=self.webpackChunklcn_frontend||[]).push([["472"],{55926:function(r,o,e){var t=e("73577"),i=e("72621"),a=(e("71695"),e("47021"),e("9065")),c=e("50778"),s=e("57243"),n=e("35359"),l=e("13823");let d,v=r=>r;const u=(0,l.T)(s.oi);class f extends u{constructor(){super(...arguments),this.value=0,this.max=1,this.indeterminate=!1,this.fourColor=!1}render(){const{ariaLabel:r}=this;return(0,s.dy)(d||(d=v`
      <div
        class="progress ${0}"
        role="progressbar"
        aria-label="${0}"
        aria-valuemin="0"
        aria-valuemax=${0}
        aria-valuenow=${0}
        >${0}</div
      >
    `),(0,n.$)(this.getRenderClasses()),r||s.Ld,this.max,this.indeterminate?s.Ld:this.value,this.renderIndicator())}getRenderClasses(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}(0,a.__decorate)([(0,c.Cb)({type:Number})],f.prototype,"value",void 0),(0,a.__decorate)([(0,c.Cb)({type:Number})],f.prototype,"max",void 0),(0,a.__decorate)([(0,c.Cb)({type:Boolean})],f.prototype,"indeterminate",void 0),(0,a.__decorate)([(0,c.Cb)({type:Boolean,attribute:"four-color"})],f.prototype,"fourColor",void 0);let m,h,p=r=>r;class g extends f{renderIndicator(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}renderDeterminateContainer(){const r=100*(1-this.value/this.max);return(0,s.dy)(m||(m=p`
      <svg viewBox="0 0 4800 4800">
        <circle class="track" pathLength="100"></circle>
        <circle
          class="active-track"
          pathLength="100"
          stroke-dashoffset=${0}></circle>
      </svg>
    `),r)}renderIndeterminateContainer(){return(0,s.dy)(h||(h=p` <div class="spinner">
      <div class="left">
        <div class="circle"></div>
      </div>
      <div class="right">
        <div class="circle"></div>
      </div>
    </div>`))}}let y;const b=(0,s.iv)(y||(y=(r=>r)`:host{--_active-indicator-color: var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width: var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color: var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color: var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color: var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color: var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size: var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;width:var(--_size);height:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.progress,.spinner,.left,.right,.circle,svg,.track,.active-track{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset 500ms cubic-bezier(0, 0, 0.2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1568.2352941176ms}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) rgba(0,0,0,0) rgba(0,0,0,0);animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-666.5ms,0ms}@media(forced-colors: active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}
`));let _=class extends g{};_.styles=[b],_=(0,a.__decorate)([(0,c.Mo)("md-circular-progress")],_);let k,x=r=>r;(0,t.Z)([(0,c.Mo)("ha-circular-progress")],(function(r,o){class e extends o{constructor(...o){super(...o),r(this)}}return{F:e,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,c.Cb)()],key:"size",value:void 0},{kind:"method",key:"updated",value:function(r){if((0,i.Z)(e,"updated",this,3)([r]),r.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,i.Z)(e,"styles",this),(0,s.iv)(k||(k=x`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `))]}}]}}),_)},68910:function(r,o,e){e.r(o),e.d(o,{ProgressDialog:function(){return v}});var t=e(73577),i=(e(71695),e(40251),e(47021),e(55926),e(57243)),a=e(50778),c=e(66193),s=e(11297);let n,l,d=r=>r,v=(0,t.Z)([(0,a.Mo)("progress-dialog")],(function(r,o){return{F:class extends o{constructor(...o){super(...o),r(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,a.IO)("ha-dialog",!0)],key:"_dialog",value:void 0},{kind:"method",key:"showDialog",value:async function(r){this._params=r,await this.updateComplete,(0,s.B)(this._dialog,"iron-resize")}},{kind:"method",key:"closeDialog",value:async function(){this.close()}},{kind:"method",key:"render",value:function(){var r,o;return this._params?(0,i.dy)(n||(n=d`
      <ha-dialog open scrimClickAction escapeKeyAction @close-dialog=${0}>
        <h2>${0}</h2>
        <p>${0}</p>

        <div id="dialog-content">
          <ha-circular-progress active></ha-circular-progress>
        </div>
      </ha-dialog>
    `),this.closeDialog,null===(r=this._params)||void 0===r?void 0:r.title,null===(o=this._params)||void 0===o?void 0:o.text):i.Ld}},{kind:"method",key:"close",value:function(){this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,(0,i.iv)(l||(l=d`
        #dialog-content {
          text-align: center;
        }
      `))]}}]}}),i.oi)}}]);
//# sourceMappingURL=472.3379d769bdda04e8.js.map