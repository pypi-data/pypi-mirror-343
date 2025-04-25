export const ids=["913"];export const modules={95:function(i,t,e){var a=e(4249),o=e(1622),s=e(7243),n=e(778),l=e(2344);(0,a.Z)([(0,n.Mo)("ha-button")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,s.iv`
      ::slotted([slot="icon"]) {
        margin-inline-start: 0px;
        margin-inline-end: 8px;
        direction: var(--direction);
        display: block;
      }
      .mdc-button {
        height: var(--button-height, 36px);
      }
      .trailing-icon {
        display: flex;
      }
      .slot-container {
        overflow: var(--button-slot-container-overflow, visible);
      }
    `]}}]}}),o.z)},1046:function(i,t,e){var a=e("4249"),o=e("7243"),s=e("778"),n=e("5359"),l=e("552"),r=e("1297"),d=e("2621"),c=e("7840"),h=e("8854");let m;c.A.addInitializer((async i=>{await i.updateComplete;const t=i;t.dialog.prepend(t.scrim),t.scrim.style.inset=0,t.scrim.style.zIndex=0;const{getOpenAnimation:e,getCloseAnimation:a}=t;t.getOpenAnimation=()=>{const i=e.call(void 0);return i.container=[...i.container??[],...i.dialog??[]],i.dialog=[],i},t.getCloseAnimation=()=>{const i=a.call(void 0);return i.container=[...i.container??[],...i.dialog??[]],i.dialog=[],i}}));(0,a.Z)([(0,s.Mo)("ha-md-dialog")],(function(i,t){class a extends t{constructor(){super(),i(this),this.addEventListener("cancel",this._handleCancel),"function"!=typeof HTMLDialogElement&&(this.addEventListener("open",this._handleOpen),m||(m=e.e("854").then(e.bind(e,5893)))),void 0===this.animate&&(this.quick=!0),void 0===this.animate&&(this.quick=!0)}}return{F:a,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:"disable-cancel-action",type:Boolean})],key:"disableCancelAction",value(){return!1}},{kind:"field",key:"_polyfillDialogRegistered",value(){return!1}},{kind:"method",key:"_handleOpen",value:async function(i){if(i.preventDefault(),this._polyfillDialogRegistered)return;this._polyfillDialogRegistered=!0,this._loadPolyfillStylesheet("/static/polyfills/dialog-polyfill.css");const t=this.shadowRoot?.querySelector("dialog");(await m).default.registerDialog(t),this.removeEventListener("open",this._handleOpen),this.show()}},{kind:"method",key:"_loadPolyfillStylesheet",value:async function(i){const t=document.createElement("link");return t.rel="stylesheet",t.href=i,new Promise(((e,a)=>{t.onload=()=>e(),t.onerror=()=>a(new Error(`Stylesheet failed to load: ${i}`)),this.shadowRoot?.appendChild(t)}))}},{kind:"method",key:"_handleCancel",value:function(i){if(this.disableCancelAction){i.preventDefault();const t=this.shadowRoot?.querySelector("dialog .container");void 0!==this.animate&&t?.animate([{transform:"rotate(-1deg)","animation-timing-function":"ease-in"},{transform:"rotate(1.5deg)","animation-timing-function":"ease-out"},{transform:"rotate(0deg)","animation-timing-function":"ease-in"}],{duration:200,iterations:2})}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,d.Z)(a,"styles",this),o.iv`
      :host {
        --md-dialog-container-color: var(--card-background-color);
        --md-dialog-headline-color: var(--primary-text-color);
        --md-dialog-supporting-text-color: var(--primary-text-color);
        --md-sys-color-scrim: #000000;

        --md-dialog-headline-weight: 400;
        --md-dialog-headline-size: 1.574rem;
        --md-dialog-supporting-text-size: 1rem;
        --md-dialog-supporting-text-line-height: 1.5rem;
      }

      :host([type="alert"]) {
        min-width: 320px;
      }

      @media all and (max-width: 450px), all and (max-height: 500px) {
        :host(:not([type="alert"])) {
          min-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          max-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          min-height: 100%;
          max-height: 100%;
          --md-dialog-container-shape: 0;
        }
      }

      ::slotted(ha-dialog-header[slot="headline"]) {
        display: contents;
      }

      .scroller {
        overflow: var(--dialog-content-overflow, auto);
      }

      slot[name="content"]::slotted(*) {
        padding: var(--dialog-content-padding, 24px);
      }
      .scrim {
        z-index: 10; /* overlay navigation */
      }
    `]}}]}}),c.A);h.I,h.G;e("8906"),e("508"),e("95"),e("596");(0,a.Z)([(0,s.Mo)("dialog-box")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_closeState",value:void 0},{kind:"field",decorators:[(0,s.IO)("ha-textfield")],key:"_textField",value:void 0},{kind:"field",decorators:[(0,s.IO)("ha-md-dialog")],key:"_dialog",value:void 0},{kind:"field",key:"_closePromise",value:void 0},{kind:"field",key:"_closeResolve",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._closePromise&&await this._closePromise,this._params=i}},{kind:"method",key:"closeDialog",value:function(){return!this._params?.confirmation&&!this._params?.prompt&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return o.Ld;const i=this._params.confirmation||this._params.prompt,t=this._params.title||this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title");return o.dy`
      <ha-md-dialog
        open
        .disableCancelAction=${i||!1}
        @closed=${this._dialogClosed}
        type="alert"
        aria-labelledby="dialog-box-title"
        aria-describedby="dialog-box-description"
      >
        <div slot="headline">
          <span .title=${t} id="dialog-box-title">
            ${this._params.warning?o.dy`<ha-svg-icon
                  .path=${"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16"}
                  style="color: var(--warning-color)"
                ></ha-svg-icon> `:o.Ld}
            ${t}
          </span>
        </div>
        <div slot="content" id="dialog-box-description">
          ${this._params.text?o.dy` <p>${this._params.text}</p> `:""}
          ${this._params.prompt?o.dy`
                <ha-textfield
                  dialogInitialFocus
                  value=${(0,l.o)(this._params.defaultValue)}
                  .placeholder=${this._params.placeholder}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                  .min=${this._params.inputMin}
                  .max=${this._params.inputMax}
                ></ha-textfield>
              `:""}
        </div>
        <div slot="actions">
          ${i&&o.dy`
            <ha-button
              @click=${this._dismiss}
              ?dialogInitialFocus=${!this._params.prompt&&this._params.destructive}
            >
              ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
            </ha-button>
          `}
          <ha-button
            @click=${this._confirm}
            ?dialogInitialFocus=${!this._params.prompt&&!this._params.destructive}
            class=${(0,n.$)({destructive:this._params.destructive||!1})}
          >
            ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
          </ha-button>
        </div>
      </ha-md-dialog>
    `}},{kind:"method",key:"_cancel",value:function(){this._params?.cancel&&this._params.cancel()}},{kind:"method",key:"_dismiss",value:function(){this._closeState="canceled",this._cancel(),this._closeDialog()}},{kind:"method",key:"_confirm",value:function(){this._closeState="confirmed",this._params.confirm&&this._params.confirm(this._textField?.value),this._closeDialog()}},{kind:"method",key:"_closeDialog",value:function(){(0,r.B)(this,"dialog-closed",{dialog:this.localName}),this._dialog?.close(),this._closePromise=new Promise((i=>{this._closeResolve=i}))}},{kind:"method",key:"_dialogClosed",value:function(){this._closeState||((0,r.B)(this,"dialog-closed",{dialog:this.localName}),this._cancel()),this._closeState=void 0,this._params=void 0,this._closeResolve?.(),this._closeResolve=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
      :host([inert]) {
        pointer-events: initial !important;
        cursor: initial !important;
      }
      a {
        color: var(--primary-color);
      }
      p {
        margin: 0;
        color: var(--primary-text-color);
      }
      .no-bottom-padding {
        padding-bottom: 0;
      }
      .secondary {
        color: var(--secondary-text-color);
      }
      .destructive {
        --mdc-theme-primary: var(--error-color);
      }
      ha-textfield {
        width: 100%;
      }
    `}}]}}),o.oi)}};
//# sourceMappingURL=913.4ebab0fee9a4cb0a.js.map