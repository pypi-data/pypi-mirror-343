"use strict";(self.webpackChunklcn_frontend=self.webpackChunklcn_frontend||[]).push([["71"],{52158:function(e,t,i){var a=i(73577),n=(i(71695),i(47021),i(4918)),l=i(6394),s=i(57243),o=i(50778),d=i(35359),r=i(11297);let c,u,h=e=>e;(0,a.Z)([(0,o.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,s.dy)(c||(c=h` <div class="mdc-form-field ${0}">
      <slot></slot>
      <label class="mdc-label" @click=${0}>
        <slot name="label">${0}</slot>
      </label>
    </div>`),(0,d.$)(e),this._labelClick,this.label)}},{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,r.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,r.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value(){return[l.W,(0,s.iv)(u||(u=h`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field {
        align-items: var(--ha-formfield-align-items, center);
        gap: 4px;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding: 0;
      }
      :host([disabled]) label {
        color: var(--disabled-text-color);
      }
    `))]}}]}}),n.a)},74064:function(e,t,i){i.d(t,{M:function(){return v}});var a=i(73577),n=i(72621),l=(i(71695),i(47021),i(65703)),s=i(46289),o=i(57243),d=i(50778);let r,c,u,h=e=>e,v=(0,a.Z)([(0,d.Mo)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,n.Z)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[s.W,(0,o.iv)(r||(r=h`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `)),"rtl"===document.dir?(0,o.iv)(c||(c=h`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `)):(0,o.iv)(u||(u=h``))]}}]}}),l.K)},61631:function(e,t,i){var a=i(73577),n=(i(71695),i(47021),i(5601)),l=i(81577),s=i(57243),o=i(50778);let d,r=e=>e;(0,a.Z)([(0,o.Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,(0,s.iv)(d||(d=r`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `))]}}]}}),n.J)},37768:function(e,t,i){i.r(t),i.d(t,{CreateEntityDialog:()=>De});var a=i("73577"),n=(i("71695"),i("40251"),i("39527"),i("67670"),i("13334"),i("47021"),i("60738")),l=i("65378"),s=(i("59897"),i("74064"),i("72621")),o=i("60930"),d=i("9714"),r=i("57243"),c=i("50778"),u=i("56587"),h=i("30137");let v,m,p,k,_=e=>e;(0,a.Z)([(0,c.Mo)("ha-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,c.Cb)({type:Boolean,reflect:!0})],key:"clearable",value(){return!1}},{kind:"field",decorators:[(0,c.Cb)({attribute:"inline-arrow",type:Boolean})],key:"inlineArrow",value(){return!1}},{kind:"method",key:"render",value:function(){return(0,r.dy)(v||(v=_`
      ${0}
      ${0}
    `),(0,s.Z)(i,"render",this,3)([]),this.clearable&&!this.required&&!this.disabled&&this.value?(0,r.dy)(m||(m=_`<ha-icon-button
            label="clear"
            @click=${0}
            .path=${0}
          ></ha-icon-button>`),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):r.Ld)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,r.dy)(p||(p=_`<span class="mdc-select__icon"
      ><slot name="icon"></slot
    ></span>`)):r.Ld}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"firstUpdated",value:async function(){var e;((0,s.Z)(i,"firstUpdated",this,3)([]),this.inlineArrow)&&(null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector(".mdc-select__selected-text-container"))||void 0===e||e.classList.add("inline-arrow"))}},{kind:"method",key:"updated",value:function(e){if((0,s.Z)(i,"updated",this,3)([e]),e.has("inlineArrow")){var t;const e=null===(t=this.shadowRoot)||void 0===t?void 0:t.querySelector(".mdc-select__selected-text-container");this.inlineArrow?null==e||e.classList.add("inline-arrow"):null==e||e.classList.remove("inline-arrow")}}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.Z)(i,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value(){return(0,u.D)((async()=>{await(0,h.y)(),this.layoutOptions()}),500)}},{kind:"field",static:!0,key:"styles",value(){return[d.W,(0,r.iv)(k||(k=_`
      :host([clearable]) {
        position: relative;
      }
      .mdc-select:not(.mdc-select--disabled) .mdc-select__icon {
        color: var(--secondary-text-color);
      }
      .mdc-select__anchor {
        width: var(--ha-select-min-width, 200px);
      }
      .mdc-select--filled .mdc-select__anchor {
        height: var(--ha-select-height, 56px);
      }
      .mdc-select--filled .mdc-floating-label {
        inset-inline-start: 12px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label {
        inset-inline-start: 48px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select .mdc-select__anchor {
        padding-inline-start: 12px;
        padding-inline-end: 0px;
        direction: var(--direction);
      }
      .mdc-select__anchor .mdc-floating-label--float-above {
        transform-origin: var(--float-start);
      }
      .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 0px);
      }
      :host([clearable]) .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
      }
      ha-icon-button {
        position: absolute;
        top: 10px;
        right: 28px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: 28px;
        direction: var(--direction);
      }
      .inline-arrow {
        flex-grow: 0;
      }
    `))]}}]}}),o.K);var y=i("11297"),g=i("44118");const f=e=>e.stopPropagation();var b=i("66193"),$=i("75167");let T,C,x,R,A=e=>e;(0,a.Z)([(0,c.Mo)("lcn-config-binary-sensor-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{source:"BINSENSOR1"}}},{kind:"field",decorators:[(0,c.SB)()],key:"_sourceType",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,c.IO)("#source-select")],key:"_sourceSelect",value:void 0},{kind:"get",key:"_binsensorPorts",value:function(){const e=this.lcn.localize("binary-sensor");return[{name:e+" 1",value:"BINSENSOR1"},{name:e+" 2",value:"BINSENSOR2"},{name:e+" 3",value:"BINSENSOR3"},{name:e+" 4",value:"BINSENSOR4"},{name:e+" 5",value:"BINSENSOR5"},{name:e+" 6",value:"BINSENSOR6"},{name:e+" 7",value:"BINSENSOR7"},{name:e+" 8",value:"BINSENSOR8"}]}},{kind:"get",key:"_regulators",value:function(){const e=this.lcn.localize("regulator");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"field",key:"_keys",value(){return[{name:"A1",value:"A1"},{name:"A2",value:"A2"},{name:"A3",value:"A3"},{name:"A4",value:"A4"},{name:"A5",value:"A5"},{name:"A6",value:"A6"},{name:"A7",value:"A7"},{name:"A8",value:"A8"},{name:"B1",value:"B1"},{name:"B2",value:"B2"},{name:"B3",value:"B3"},{name:"B4",value:"B4"},{name:"B5",value:"B5"},{name:"B6",value:"B6"},{name:"B7",value:"B7"},{name:"B8",value:"B8"},{name:"C1",value:"C1"},{name:"C2",value:"C2"},{name:"C3",value:"C3"},{name:"C4",value:"C4"},{name:"C5",value:"C5"},{name:"C6",value:"C6"},{name:"C7",value:"C7"},{name:"C8",value:"C8"},{name:"D1",value:"D1"},{name:"D2",value:"D2"},{name:"D3",value:"D3"},{name:"D4",value:"D4"},{name:"D5",value:"D5"},{name:"D6",value:"D6"},{name:"D7",value:"D7"},{name:"D8",value:"D8"}]}},{kind:"get",key:"_sourceTypes",value:function(){return[{name:this.lcn.localize("binsensors"),value:this._binsensorPorts,id:"binsensors"},{name:this.lcn.localize("regulator-locks"),value:this._regulators,id:"regulator-locks"},{name:this.lcn.localize("key-locks"),value:this._keys,id:"key-locks"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._sourceType=this._sourceTypes[0],this._source=this._sourceType.value[0]}},{kind:"method",key:"render",value:function(){return this._sourceType||this._source?(0,r.dy)(T||(T=A`
      <div class="sources">
        <ha-select
          id="source-type-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-select
          id="source-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
      </div>
    `),this.lcn.localize("source-type"),this._sourceType.id,this._sourceTypeChanged,f,this._sourceTypes.map((e=>(0,r.dy)(C||(C=A`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.id,e.name))),this.lcn.localize("source"),this._source.value,this._sourceChanged,f,this._sourceType.value.map((e=>(0,r.dy)(x||(x=A`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name)))):r.Ld}},{kind:"method",key:"_sourceTypeChanged",value:function(e){const t=e.target;-1!==t.index&&(this._sourceType=this._sourceTypes.find((e=>e.id===t.value)),this._source=this._sourceType.value[0],this._sourceSelect.select(-1))}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sourceType.value.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(R||(R=A`
        .sources {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),r.oi);i("11740"),i("70596");var D=i("62523"),L=i("83835");let S,w=e=>e;(0,a.Z)([(0,c.Mo)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,s.Z)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{var e;this.haptic&&(e="light",(0,y.B)(window,"haptic",e))}))}},{kind:"field",static:!0,key:"styles",value(){return[L.W,(0,r.iv)(S||(S=w`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `))]}}]}}),D.H);i("14394");let z,E,O,B,P,V,M=e=>e;(0,a.Z)([(0,c.Mo)("lcn-config-climate-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1,type:Number})],key:"softwareSerial",value(){return-1}},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{source:"VAR1",setpoint:"R1VARSETPOINT",max_temp:35,min_temp:7,lockable:!1,target_value_locked:-1,unit_of_measurement:"°C"}}},{kind:"field",decorators:[(0,c.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_setpoint",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_unit",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_lockOption",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_targetValueLocked",value(){return 0}},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_is2012",value:function(){return this.softwareSerial>=1441792}},{kind:"get",key:"_variablesNew",value:function(){const e=this.lcn.localize("variable");return[{name:e+" 1",value:"VAR1"},{name:e+" 2",value:"VAR2"},{name:e+" 3",value:"VAR3"},{name:e+" 4",value:"VAR4"},{name:e+" 5",value:"VAR5"},{name:e+" 6",value:"VAR6"},{name:e+" 7",value:"VAR7"},{name:e+" 8",value:"VAR8"},{name:e+" 9",value:"VAR9"},{name:e+" 10",value:"VAR10"},{name:e+" 11",value:"VAR11"},{name:e+" 12",value:"VAR12"}]}},{kind:"field",key:"_variablesOld",value(){return[{name:"TVar",value:"TVAR"},{name:"R1Var",value:"R1VAR"},{name:"R2Var",value:"R2VAR"}]}},{kind:"get",key:"_varSetpoints",value:function(){const e=this.lcn.localize("setpoint");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"field",key:"_varUnits",value(){return[{name:"Celsius",value:"°C"},{name:"Fahrenheit",value:"°F"}]}},{kind:"get",key:"_regulatorLockOptions",value:function(){const e=[{name:this.lcn.localize("dashboard-entities-dialog-climate-regulator-not-lockable"),value:"NOT_LOCKABLE"},{name:this.lcn.localize("dashboard-entities-dialog-climate-regulator-lockable"),value:"LOCKABLE"},{name:this.lcn.localize("dashboard-entities-dialog-climate-regulator-lockable-with-target-value"),value:"LOCKABLE_WITH_TARGET_VALUE"}];return this.softwareSerial<1180417?e.slice(0,2):e}},{kind:"get",key:"_sources",value:function(){return this._is2012?this._variablesNew:this._variablesOld}},{kind:"get",key:"_setpoints",value:function(){return this._is2012?this._varSetpoints.concat(this._variablesNew):this._varSetpoints}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._source=this._sources[0],this._setpoint=this._setpoints[0],this._unit=this._varUnits[0],this._lockOption=this._regulatorLockOptions[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,s.Z)(i,"willUpdate",this,3)([e]),this._invalid=!this._validateMinTemp(this.domainData.min_temp)||!this._validateMaxTemp(this.domainData.max_temp)||!this._validateTargetValueLocked(this._targetValueLocked)}},{kind:"method",key:"update",value:function(e){(0,s.Z)(i,"update",this,3)([e]),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._source&&this._setpoint&&this._unit&&this._lockOption?(0,r.dy)(z||(z=M`
      <div class="sources">
        <ha-select
          id="source-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-select
          id="setpoint-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
      </div>

      <ha-select
        id="unit-select"
        .label=${0}
        .value=${0}
        fixedMenuPosition
        @selected=${0}
        @closed=${0}
      >
        ${0}
      </ha-select>

      <div class="temperatures">
        <ha-textfield
          id="min-temperature"
          .label=${0}
          type="number"
          .suffix=${0}
          .value=${0}
          required
          autoValidate
          @input=${0}
          .validityTransform=${0}
          .validationMessage=${0}
        ></ha-textfield>

        <ha-textfield
          id="max-temperature"
          .label=${0}
          type="number"
          .suffix=${0}
          .value=${0}
          required
          autoValidate
          @input=${0}
          .validityTransform=${0}
          .validationMessage=${0}
        ></ha-textfield>
      </div>

      <div class="lock-options">
        <ha-select
          id="lock-options-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-textfield
          id="target-value"
          .label=${0}
          type="number"
          suffix="%"
          .value=${0}
          .disabled=${0}
          .helper=${0}
          .helperPersistent=${0}
          required
          autoValidate
          @input=${0}
          .validityTransform=${0}
          .validationMessage=${0}
        >
        </ha-textfield>
      </div>
    `),this.lcn.localize("source"),this._source.value,this._sourceChanged,f,this._sources.map((e=>(0,r.dy)(E||(E=M`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name))),this.lcn.localize("setpoint"),this._setpoint.value,this._setpointChanged,f,this._setpoints.map((e=>(0,r.dy)(O||(O=M`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name))),this.lcn.localize("dashboard-entities-dialog-unit-of-measurement"),this._unit.value,this._unitChanged,f,this._varUnits.map((e=>(0,r.dy)(B||(B=M` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name))),this.lcn.localize("dashboard-entities-dialog-climate-min-temperature"),this._unit.value,this.domainData.min_temp.toString(),this._minTempChanged,this._validityTransformMinTemp,this.lcn.localize("dashboard-entities-dialog-climate-min-temperature-error"),this.lcn.localize("dashboard-entities-dialog-climate-max-temperature"),this._unit.value,this.domainData.max_temp.toString(),this._maxTempChanged,this._validityTransformMaxTemp,this.lcn.localize("dashboard-entities-dialog-climate-max-temperature-error"),this.lcn.localize("dashboard-entities-dialog-climate-regulator-lock"),this._lockOption.value,this._lockOptionChanged,f,this._regulatorLockOptions.map((e=>(0,r.dy)(P||(P=M`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name))),this.lcn.localize("dashboard-entities-dialog-climate-target-value"),this._targetValueLocked.toString(),"LOCKABLE_WITH_TARGET_VALUE"!==this._lockOption.value,this.lcn.localize("dashboard-entities-dialog-climate-target-value-helper"),"LOCKABLE_WITH_TARGET_VALUE"===this._lockOption.value,this._targetValueLockedChanged,this._validityTransformTargetValueLocked,this.lcn.localize("dashboard-entities-dialog-climate-target-value-error")):r.Ld}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sources.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"method",key:"_setpointChanged",value:function(e){const t=e.target;-1!==t.index&&(this._setpoint=this._setpoints.find((e=>e.value===t.value)),this.domainData.setpoint=this._setpoint.value)}},{kind:"method",key:"_minTempChanged",value:function(e){const t=e.target;this.domainData.min_temp=+t.value;this.shadowRoot.querySelector("#max-temperature").reportValidity(),this.requestUpdate()}},{kind:"method",key:"_maxTempChanged",value:function(e){const t=e.target;this.domainData.max_temp=+t.value;this.shadowRoot.querySelector("#min-temperature").reportValidity(),this.requestUpdate()}},{kind:"method",key:"_unitChanged",value:function(e){const t=e.target;-1!==t.index&&(this._unit=this._varUnits.find((e=>e.value===t.value)),this.domainData.unit_of_measurement=this._unit.value)}},{kind:"method",key:"_lockOptionChanged",value:function(e){const t=e.target;switch(-1===t.index?this._lockOption=this._regulatorLockOptions[0]:this._lockOption=this._regulatorLockOptions.find((e=>e.value===t.value)),this._lockOption.value){case"LOCKABLE":this.domainData.lockable=!0,this.domainData.target_value_locked=-1;break;case"LOCKABLE_WITH_TARGET_VALUE":this.domainData.lockable=!0,this.domainData.target_value_locked=this._targetValueLocked;break;default:this.domainData.lockable=!1,this.domainData.target_value_locked=-1}}},{kind:"method",key:"_targetValueLockedChanged",value:function(e){const t=e.target;this._targetValueLocked=+t.value,this.domainData.target_value_locked=+t.value}},{kind:"method",key:"_validateMaxTemp",value:function(e){return e>this.domainData.min_temp}},{kind:"method",key:"_validateMinTemp",value:function(e){return e<this.domainData.max_temp}},{kind:"method",key:"_validateTargetValueLocked",value:function(e){return e>=0&&e<=100}},{kind:"get",key:"_validityTransformMaxTemp",value:function(){return e=>({valid:this._validateMaxTemp(+e)})}},{kind:"get",key:"_validityTransformMinTemp",value:function(){return e=>({valid:this._validateMinTemp(+e)})}},{kind:"get",key:"_validityTransformTargetValueLocked",value:function(){return e=>({valid:this._validateTargetValueLocked(+e)})}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(V||(V=M`
        .sources,
        .temperatures,
        .lock-options {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),r.oi);i("56071"),i("50722");let U,N,I,Z,H,Y,F,q=e=>e;(0,a.Z)([(0,c.Mo)("lcn-config-cover-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{motor:"MOTOR1",positioning_mode:"NONE",reverse_time:"RT1200"}}},{kind:"field",decorators:[(0,c.SB)()],key:"_motor",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_positioningMode",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_reverseDelay",value:void 0},{kind:"get",key:"_motors",value:function(){return[{name:this.lcn.localize("motor-port",{port:1}),value:"MOTOR1"},{name:this.lcn.localize("motor-port",{port:2}),value:"MOTOR2"},{name:this.lcn.localize("motor-port",{port:3}),value:"MOTOR3"},{name:this.lcn.localize("motor-port",{port:4}),value:"MOTOR4"},{name:this.lcn.localize("outputs"),value:"OUTPUTS"}]}},{kind:"field",key:"_reverseDelays",value(){return[{name:"70ms",value:"RT70"},{name:"600ms",value:"RT600"},{name:"1200ms",value:"RT1200"}]}},{kind:"get",key:"_positioningModes",value:function(){return[{name:this.lcn.localize("motor-positioning-none"),value:"NONE"},{name:this.lcn.localize("motor-positioning-bs4"),value:"BS4"},{name:this.lcn.localize("motor-positioning-module"),value:"MODULE"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._motor=this._motors[0],this._positioningMode=this._positioningModes[0],this._reverseDelay=this._reverseDelays[0]}},{kind:"method",key:"render",value:function(){return this._motor||this._positioningMode||this._reverseDelay?(0,r.dy)(U||(U=q`
      <ha-select
        id="motor-select"
        .label=${0}
        .value=${0}
        fixedMenuPosition
        @selected=${0}
        @closed=${0}
      >
        ${0}
      </ha-select>

      ${0}
    `),this.lcn.localize("motor"),this._motor.value,this._motorChanged,f,this._motors.map((e=>(0,r.dy)(N||(N=q` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name))),"OUTPUTS"===this._motor.value?(0,r.dy)(I||(I=q`
            <ha-select
              id="reverse-delay-select"
              .label=${0}
              .value=${0}
              fixedMenuPosition
              @selected=${0}
              @closed=${0}
            >
              ${0}
            </ha-select>
          `),this.lcn.localize("reverse-delay"),this._reverseDelay.value,this._reverseDelayChanged,f,this._reverseDelays.map((e=>(0,r.dy)(Z||(Z=q`
                  <ha-list-item .value=${0}> ${0} </ha-list-item>
                `),e.value,e.name)))):(0,r.dy)(H||(H=q`
            <ha-select
              id="positioning-mode-select"
              .label=${0}
              .value=${0}
              fixedMenuPosition
              @selected=${0}
              @closed=${0}
            >
              ${0}
            </ha-select>
          `),this.lcn.localize("motor-positioning-mode"),this._positioningMode.value,this._positioningModeChanged,f,this._positioningModes.map((e=>(0,r.dy)(Y||(Y=q`
                  <ha-list-item .value=${0}>
                    ${0}
                  </ha-list-item>
                `),e.value,e.name))))):r.Ld}},{kind:"method",key:"_motorChanged",value:function(e){const t=e.target;-1!==t.index&&(this._motor=this._motors.find((e=>e.value===t.value)),this._positioningMode=this._positioningModes[0],this._reverseDelay=this._reverseDelays[0],this.domainData.motor=this._motor.value,"OUTPUTS"===this._motor.value?this.domainData.positioning_mode="NONE":this.domainData.reverse_time="RT1200")}},{kind:"method",key:"_positioningModeChanged",value:function(e){const t=e.target;-1!==t.index&&(this._positioningMode=this._positioningModes.find((e=>e.value===t.value)),this.domainData.positioning_mode=this._positioningMode.value)}},{kind:"method",key:"_reverseDelayChanged",value:function(e){const t=e.target;-1!==t.index&&(this._reverseDelay=this._reverseDelays.find((e=>e.value===t.value)),this.domainData.reverse_time=this._reverseDelay.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(F||(F=q`
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),r.oi);i("61631"),i("52158");let K,W,G,X,j=e=>e;(0,a.Z)([(0,c.Mo)("lcn-config-light-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{output:"OUTPUT1",dimmable:!1,transition:0}}},{kind:"field",decorators:[(0,c.SB)()],key:"_portType",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_port",value:void 0},{kind:"field",decorators:[(0,c.IO)("#port-select")],key:"_portSelect",value:void 0},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"get",key:"_portTypes",value:function(){return[{name:this.lcn.localize("output"),value:this._outputPorts,id:"output"},{name:this.lcn.localize("relay"),value:this._relayPorts,id:"relay"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._portType=this._portTypes[0],this._port=this._portType.value[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,s.Z)(i,"willUpdate",this,3)([e]),this._invalid=!this._validateTransition(this.domainData.transition)}},{kind:"method",key:"update",value:function(e){(0,s.Z)(i,"update",this,3)([e]),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._portType||this._port?(0,r.dy)(K||(K=j`
      <div id="port-type">${0}</div>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="output"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="relay"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-select
        id="port-select"
        .label=${0}
        .value=${0}
        fixedMenuPosition
        @selected=${0}
        @closed=${0}
      >
        ${0}
      </ha-select>

      ${0}
    `),this.lcn.localize("port-type"),this.lcn.localize("output"),"output"===this._portType.id,this._portTypeChanged,this.lcn.localize("relay"),"relay"===this._portType.id,this._portTypeChanged,this.lcn.localize("port"),this._port.value,this._portChanged,f,this._portType.value.map((e=>(0,r.dy)(W||(W=j` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name))),this._renderOutputFeatures()):r.Ld}},{kind:"method",key:"_renderOutputFeatures",value:function(){return"output"===this._portType.id?(0,r.dy)(G||(G=j`
          <div id="dimmable">
            <label>${0}:</label>

            <ha-switch
              .checked=${0}
              @change=${0}
            ></ha-switch>
          </div>

          <ha-textfield
            id="transition"
            .label=${0}
            type="number"
            suffix="s"
            .value=${0}
            min="0"
            max="486"
            required
            autoValidate
            @input=${0}
            .validityTransform=${0}
            .validationMessage=${0}
          ></ha-textfield>
        `),this.lcn.localize("dashboard-entities-dialog-light-dimmable"),this.domainData.dimmable,this._dimmableChanged,this.lcn.localize("dashboard-entities-dialog-light-transition"),this.domainData.transition.toString(),this._transitionChanged,this._validityTransformTransition,this.lcn.localize("dashboard-entities-dialog-light-transition-error")):r.Ld}},{kind:"method",key:"_portTypeChanged",value:function(e){const t=e.target;this._portType=this._portTypes.find((e=>e.id===t.value)),this._port=this._portType.value[0],this._portSelect.select(-1)}},{kind:"method",key:"_portChanged",value:function(e){const t=e.target;-1!==t.index&&(this._port=this._portType.value.find((e=>e.value===t.value)),this.domainData.output=this._port.value)}},{kind:"method",key:"_dimmableChanged",value:function(e){this.domainData.dimmable=e.target.checked}},{kind:"method",key:"_transitionChanged",value:function(e){const t=e.target;this.domainData.transition=+t.value,this.requestUpdate()}},{kind:"method",key:"_validateTransition",value:function(e){return e>=0&&e<=486}},{kind:"get",key:"_validityTransformTransition",value:function(){return e=>({valid:this._validateTransition(+e)})}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(X||(X=j`
        #port-type {
          margin-top: 16px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        #dimmable {
          margin-top: 16px;
        }
        #transition {
          margin-top: 16px;
        }
      `))]}}]}}),r.oi);i("19083"),i("92745"),i("61006"),i("99790"),i("76418");let J,Q,ee,te,ie,ae,ne,le,se,oe,de,re,ce,ue,he=e=>e,ve=((0,a.Z)([(0,c.Mo)("lcn-config-scene-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{register:0,scene:0,outputs:[],transition:0}}},{kind:"field",decorators:[(0,c.SB)()],key:"_register",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_scene",value:void 0},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_registers",value:function(){const e=this.lcn.localize("register");return[{name:e+" 0",value:"0"},{name:e+" 1",value:"1"},{name:e+" 2",value:"2"},{name:e+" 3",value:"3"},{name:e+" 4",value:"4"},{name:e+" 5",value:"5"},{name:e+" 6",value:"6"},{name:e+" 7",value:"7"},{name:e+" 8",value:"8"},{name:e+" 9",value:"9"}]}},{kind:"get",key:"_scenes",value:function(){const e=this.lcn.localize("scene");return[{name:e+" 1",value:"0"},{name:e+" 2",value:"1"},{name:e+" 3",value:"2"},{name:e+" 4",value:"3"},{name:e+" 5",value:"4"},{name:e+" 6",value:"5"},{name:e+" 7",value:"6"},{name:e+" 8",value:"7"},{name:e+" 9",value:"8"},{name:e+" 10",value:"9"}]}},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._register=this._registers[0],this._scene=this._scenes[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,s.Z)(i,"willUpdate",this,3)([e]),this._invalid=!this._validateTransition(this.domainData.transition)}},{kind:"method",key:"update",value:function(e){(0,s.Z)(i,"update",this,3)([e]),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._register||this._scene?(0,r.dy)(J||(J=he`
      <div class="registers">
        <ha-select
          id="register-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-select
          id="scene-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
      </div>

      <div class="ports">
        <label>${0}:</label><br />
        ${0}
      </div>

      <div class="ports">
        <label>${0}:</label><br />
        ${0}
      </div>

      <ha-textfield
        .label=${0}
        type="number"
        suffix="s"
        .value=${0}
        min="0"
        max="486"
        required
        autoValidate
        @input=${0}
        .validityTransform=${0}
        .disabled=${0}
        .validationMessage=${0}
      ></ha-textfield>
    `),this.lcn.localize("register"),this._register.value,this._registerChanged,f,this._registers.map((e=>(0,r.dy)(Q||(Q=he`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name))),this.lcn.localize("scene"),this._scene.value,this._sceneChanged,f,this._scenes.map((e=>(0,r.dy)(ee||(ee=he` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name))),this.lcn.localize("outputs"),this._outputPorts.map((e=>(0,r.dy)(te||(te=he`
            <ha-formfield label=${0}>
              <ha-checkbox .value=${0} @change=${0}></ha-checkbox>
            </ha-formfield>
          `),e.name,e.value,this._portCheckedChanged))),this.lcn.localize("relays"),this._relayPorts.map((e=>(0,r.dy)(ie||(ie=he`
            <ha-formfield label=${0}>
              <ha-checkbox .value=${0} @change=${0}></ha-checkbox>
            </ha-formfield>
          `),e.name,e.value,this._portCheckedChanged))),this.lcn.localize("dashboard-entities-dialog-scene-transition"),this.domainData.transition.toString(),this._transitionChanged,this._validityTransformTransition,this._transitionDisabled,this.lcn.localize("dashboard-entities-dialog-scene-transition-error")):r.Ld}},{kind:"method",key:"_registerChanged",value:function(e){const t=e.target;-1!==t.index&&(this._register=this._registers.find((e=>e.value===t.value)),this.domainData.register=+this._register.value)}},{kind:"method",key:"_sceneChanged",value:function(e){const t=e.target;-1!==t.index&&(this._scene=this._scenes.find((e=>e.value===t.value)),this.domainData.scene=+this._scene.value)}},{kind:"method",key:"_portCheckedChanged",value:function(e){e.target.checked?this.domainData.outputs.push(e.target.value):this.domainData.outputs=this.domainData.outputs.filter((t=>e.target.value!==t)),this.requestUpdate()}},{kind:"method",key:"_transitionChanged",value:function(e){const t=e.target;this.domainData.transition=+t.value,this.requestUpdate()}},{kind:"method",key:"_validateTransition",value:function(e){return e>=0&&e<=486}},{kind:"get",key:"_validityTransformTransition",value:function(){return e=>({valid:this._validateTransition(+e)})}},{kind:"get",key:"_transitionDisabled",value:function(){const e=this._outputPorts.map((e=>e.value));return 0===this.domainData.outputs.filter((t=>e.includes(t))).length}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(ae||(ae=he`
        .registers {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        .ports {
          margin-top: 10px;
        }
      `))]}}]}}),r.oi),e=>e),me=((0,a.Z)([(0,c.Mo)("lcn-config-sensor-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1,type:Number})],key:"softwareSerial",value(){return-1}},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{source:"VAR1",unit_of_measurement:"NATIVE"}}},{kind:"field",decorators:[(0,c.SB)()],key:"_sourceType",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_unit",value:void 0},{kind:"field",decorators:[(0,c.IO)("#source-select")],key:"_sourceSelect",value:void 0},{kind:"get",key:"_is2013",value:function(){return this.softwareSerial>=1507846}},{kind:"field",key:"_variablesOld",value(){return[{name:"TVar",value:"TVAR"},{name:"R1Var",value:"R1VAR"},{name:"R2Var",value:"R2VAR"}]}},{kind:"get",key:"_variablesNew",value:function(){const e=this.lcn.localize("variable");return[{name:e+" 1",value:"VAR1"},{name:e+" 2",value:"VAR2"},{name:e+" 3",value:"VAR3"},{name:e+" 4",value:"VAR4"},{name:e+" 5",value:"VAR5"},{name:e+" 6",value:"VAR6"},{name:e+" 7",value:"VAR7"},{name:e+" 8",value:"VAR8"},{name:e+" 9",value:"VAR9"},{name:e+" 10",value:"VAR10"},{name:e+" 11",value:"VAR11"},{name:e+" 12",value:"VAR12"}]}},{kind:"get",key:"_setpoints",value:function(){const e=this.lcn.localize("setpoint");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"get",key:"_thresholdsOld",value:function(){const e=this.lcn.localize("threshold");return[{name:e+" 1",value:"THRS1"},{name:e+" 2",value:"THRS2"},{name:e+" 3",value:"THRS3"},{name:e+" 4",value:"THRS4"},{name:e+" 5",value:"THRS5"}]}},{kind:"get",key:"_thresholdsNew",value:function(){const e=this.lcn.localize("threshold");return[{name:e+" 1-1",value:"THRS1"},{name:e+" 1-2",value:"THRS2"},{name:e+" 1-3",value:"THRS3"},{name:e+" 1-4",value:"THRS4"},{name:e+" 2-1",value:"THRS2_1"},{name:e+" 2-2",value:"THRS2_2"},{name:e+" 2-3",value:"THRS2_3"},{name:e+" 2-4",value:"THRS2_4"},{name:e+" 3-1",value:"THRS3_1"},{name:e+" 3-2",value:"THRS3_2"},{name:e+" 3-3",value:"THRS3_3"},{name:e+" 3-4",value:"THRS3_4"},{name:e+" 4-1",value:"THRS4_1"},{name:e+" 4-2",value:"THRS4_2"},{name:e+" 4-3",value:"THRS4_3"},{name:e+" 4-4",value:"THRS4_4"}]}},{kind:"get",key:"_s0Inputs",value:function(){const e=this.lcn.localize("s0input");return[{name:e+" 1",value:"S0INPUT1"},{name:e+" 2",value:"S0INPUT2"},{name:e+" 3",value:"S0INPUT3"},{name:e+" 4",value:"S0INPUT4"}]}},{kind:"get",key:"_ledPorts",value:function(){const e=this.lcn.localize("led");return[{name:e+" 1",value:"LED1"},{name:e+" 2",value:"LED2"},{name:e+" 3",value:"LED3"},{name:e+" 4",value:"LED4"},{name:e+" 5",value:"LED5"},{name:e+" 6",value:"LED6"},{name:e+" 7",value:"LED7"},{name:e+" 8",value:"LED8"},{name:e+" 9",value:"LED9"},{name:e+" 10",value:"LED10"},{name:e+" 11",value:"LED11"},{name:e+" 12",value:"LED12"}]}},{kind:"get",key:"_logicOpPorts",value:function(){const e=this.lcn.localize("logic");return[{name:e+" 1",value:"LOGICOP1"},{name:e+" 2",value:"LOGICOP2"},{name:e+" 3",value:"LOGICOP3"},{name:e+" 4",value:"LOGICOP4"}]}},{kind:"get",key:"_sourceTypes",value:function(){return[{name:this.lcn.localize("variables"),value:this._is2013?this._variablesNew:this._variablesOld,id:"variables"},{name:this.lcn.localize("setpoints"),value:this._setpoints,id:"setpoints"},{name:this.lcn.localize("thresholds"),value:this._is2013?this._thresholdsNew:this._thresholdsOld,id:"thresholds"},{name:this.lcn.localize("s0inputs"),value:this._s0Inputs,id:"s0inputs"},{name:this.lcn.localize("leds"),value:this._ledPorts,id:"ledports"},{name:this.lcn.localize("logics"),value:this._logicOpPorts,id:"logicopports"}]}},{kind:"get",key:"_varUnits",value:function(){return[{name:this.lcn.localize("unit-lcn-native"),value:"NATIVE"},{name:"Celsius",value:"°C"},{name:"Fahrenheit",value:"°F"},{name:"Kelvin",value:"K"},{name:"Lux (T-Port)",value:"LUX_T"},{name:"Lux (I-Port)",value:"LUX_I"},{name:this.lcn.localize("unit-humidity")+" (%)",value:"PERCENT"},{name:"CO2 (‰)",value:"PPM"},{name:this.lcn.localize("unit-wind")+" (m/s)",value:"METERPERSECOND"},{name:this.lcn.localize("unit-volts"),value:"VOLT"},{name:this.lcn.localize("unit-milliamperes"),value:"AMPERE"},{name:this.lcn.localize("unit-angle")+" (°)",value:"DEGREE"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._sourceType=this._sourceTypes[0],this._source=this._sourceType.value[0],this._unit=this._varUnits[0]}},{kind:"method",key:"render",value:function(){return this._sourceType||this._source?(0,r.dy)(ne||(ne=ve`
      <div class="sources">
        <ha-select
          id="source-type-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-select
          id="source-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
      </div>

      <ha-select
        id="unit-select"
        .label=${0}
        .value=${0}
        fixedMenuPosition
        @selected=${0}
        @closed=${0}
      >
        ${0}
      </ha-select>
    `),this.lcn.localize("source-type"),this._sourceType.id,this._sourceTypeChanged,f,this._sourceTypes.map((e=>(0,r.dy)(le||(le=ve`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.id,e.name))),this.lcn.localize("source"),this._source.value,this._sourceChanged,f,this._sourceType.value.map((e=>(0,r.dy)(se||(se=ve`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.value,e.name))),this.lcn.localize("dashboard-entities-dialog-unit-of-measurement"),this._unit.value,this._unitChanged,f,this._varUnits.map((e=>(0,r.dy)(oe||(oe=ve` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name)))):r.Ld}},{kind:"method",key:"_sourceTypeChanged",value:function(e){const t=e.target;-1!==t.index&&(this._sourceType=this._sourceTypes.find((e=>e.id===t.value)),this._source=this._sourceType.value[0],this._sourceSelect.select(-1))}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sourceType.value.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"method",key:"_unitChanged",value:function(e){const t=e.target;-1!==t.index&&(this._unit=this._varUnits.find((e=>e.value===t.value)),this.domainData.unit_of_measurement=this._unit.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(de||(de=ve`
        .sources {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),r.oi),e=>e);(0,a.Z)([(0,c.Mo)("lcn-config-switch-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"domainData",value(){return{output:"OUTPUT1"}}},{kind:"field",decorators:[(0,c.SB)()],key:"_portType",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_port",value:void 0},{kind:"field",decorators:[(0,c.IO)("#port-select")],key:"_portSelect",value:void 0},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"get",key:"_regulators",value:function(){const e=this.lcn.localize("regulator");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"field",key:"_keys",value(){return[{name:"A1",value:"A1"},{name:"A2",value:"A2"},{name:"A3",value:"A3"},{name:"A4",value:"A4"},{name:"A5",value:"A5"},{name:"A6",value:"A6"},{name:"A7",value:"A7"},{name:"A8",value:"A8"},{name:"B1",value:"B1"},{name:"B2",value:"B2"},{name:"B3",value:"B3"},{name:"B4",value:"B4"},{name:"B5",value:"B5"},{name:"B6",value:"B6"},{name:"B7",value:"B7"},{name:"B8",value:"B8"},{name:"C1",value:"C1"},{name:"C2",value:"C2"},{name:"C3",value:"C3"},{name:"C4",value:"C4"},{name:"C5",value:"C5"},{name:"C6",value:"C6"},{name:"C7",value:"C7"},{name:"C8",value:"C8"},{name:"D1",value:"D1"},{name:"D2",value:"D2"},{name:"D3",value:"D3"},{name:"D4",value:"D4"},{name:"D5",value:"D5"},{name:"D6",value:"D6"},{name:"D7",value:"D7"},{name:"D8",value:"D8"}]}},{kind:"get",key:"_portTypes",value:function(){return[{name:this.lcn.localize("output"),value:this._outputPorts,id:"output"},{name:this.lcn.localize("relay"),value:this._relayPorts,id:"relay"},{name:this.lcn.localize("regulator"),value:this._regulators,id:"regulator-locks"},{name:this.lcn.localize("key"),value:this._keys,id:"key-locks"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)(i,"connectedCallback",this,3)([]),this._portType=this._portTypes[0],this._port=this._portType.value[0]}},{kind:"method",key:"render",value:function(){return this._portType||this._port?(0,r.dy)(re||(re=me`
      <div id="port-type">${0}</div>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="output"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="relay"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="regulator-locks"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${0}>
        <ha-radio
          name="port"
          value="key-locks"
          .checked=${0}
          @change=${0}
        ></ha-radio>
      </ha-formfield>

      <ha-select
        id="port-select"
        .label=${0}
        .value=${0}
        fixedMenuPosition
        @selected=${0}
        @closed=${0}
      >
        ${0}
      </ha-select>
    `),this.lcn.localize("port-type"),this.lcn.localize("output"),"output"===this._portType.id,this._portTypeChanged,this.lcn.localize("relay"),"relay"===this._portType.id,this._portTypeChanged,this.lcn.localize("regulator-lock"),"regulator-locks"===this._portType.id,this._portTypeChanged,this.lcn.localize("key-lock"),"key-locks"===this._portType.id,this._portTypeChanged,this._portType.name,this._port.value,this._portChanged,f,this._portType.value.map((e=>(0,r.dy)(ce||(ce=me` <ha-list-item .value=${0}> ${0} </ha-list-item> `),e.value,e.name)))):r.Ld}},{kind:"method",key:"_portTypeChanged",value:function(e){const t=e.target;this._portType=this._portTypes.find((e=>e.id===t.value)),this._port=this._portType.value[0],this._portSelect.select(-1)}},{kind:"method",key:"_portChanged",value:function(e){const t=e.target;-1!==t.index&&(this._port=this._portType.value.find((e=>e.value===t.value)),this.domainData.output=this._port.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(ue||(ue=me`
        #port-type {
          margin-top: 16px;
        }
        .lock-time {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `))]}}]}}),r.oi);var pe=i("4557");let ke,_e,ye,ge,fe,be,$e,Te,Ce,xe,Re,Ae=e=>e,De=(0,a.Z)([(0,c.Mo)("lcn-create-entity-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_name",value(){return""}},{kind:"field",decorators:[(0,c.SB)()],key:"domain",value(){return"binary_sensor"}},{kind:"field",decorators:[(0,c.SB)()],key:"_invalid",value(){return!0}},{kind:"field",decorators:[(0,c.SB)()],key:"_deviceConfig",value:void 0},{kind:"field",decorators:[(0,c.SB)(),(0,n.F_)({context:l.c,subscribe:!0})],key:"deviceConfigs",value:void 0},{kind:"get",key:"_domains",value:function(){return[{name:this.lcn.localize("binary-sensor"),domain:"binary_sensor"},{name:this.lcn.localize("climate"),domain:"climate"},{name:this.lcn.localize("cover"),domain:"cover"},{name:this.lcn.localize("light"),domain:"light"},{name:this.lcn.localize("scene"),domain:"scene"},{name:this.lcn.localize("sensor"),domain:"sensor"},{name:this.lcn.localize("switch"),domain:"switch"}]}},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this.lcn=e.lcn,this._name="",this._invalid=!0,this._deviceConfig=e.deviceConfig,this._deviceConfig||(this._deviceConfig=this.deviceConfigs[0]),await this.updateComplete}},{kind:"method",key:"render",value:function(){return this._params&&this.lcn&&this._deviceConfig?(0,r.dy)(ke||(ke=Ae`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        .heading=${0}
        @closed=${0}
      >
        <ha-select
          id="device-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>

        <ha-select
          id="domain-select"
          .label=${0}
          .value=${0}
          fixedMenuPosition
          @selected=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
        <ha-textfield
          id="name-input"
          label=${0}
          type="string"
          @input=${0}
        ></ha-textfield>

        ${0}

        <div class="buttons">
          <mwc-button
            slot="secondaryAction"
            @click=${0}
            .label=${0}
          ></mwc-button>
          <mwc-button
            slot="primaryAction"
            .disabled=${0}
            @click=${0}
            .label=${0}
          ></mwc-button>
        </div>
      </ha-dialog>
    `),(0,g.i)(this.hass,this.lcn.localize("dashboard-entities-dialog-create-title")),this._closeDialog,this.lcn.localize("device"),this._deviceConfig?(0,$.VM)(this._deviceConfig.address):void 0,this._deviceChanged,f,this.deviceConfigs.map((e=>(0,r.dy)(_e||(_e=Ae`
              <ha-list-item .value=${0}>
                <div class="primary">${0}</div>
                <div class="secondary">(${0})</div>
              </ha-list-item>
            `),(0,$.VM)(e.address),e.name,(0,$.lW)(e.address)))),this.lcn.localize("domain"),this.domain,this._domainChanged,f,this._domains.map((e=>(0,r.dy)(ye||(ye=Ae`
              <ha-list-item .value=${0}> ${0} </ha-list-item>
            `),e.domain,e.name))),this.lcn.localize("name"),this._nameChanged,this._renderDomain(this.domain),this._closeDialog,this.lcn.localize("dismiss"),this._invalid,this._create,this.lcn.localize("create")):r.Ld}},{kind:"method",key:"_renderDomain",value:function(e){if(!this._params||!this._deviceConfig)return r.Ld;switch(e){case"binary_sensor":return(0,r.dy)(ge||(ge=Ae`<lcn-config-binary-sensor-element
          id="domain"
          .hass=${0}
          .lcn=${0}
        ></lcn-config-binary-sensor-element>`),this.hass,this.lcn);case"climate":return(0,r.dy)(fe||(fe=Ae`<lcn-config-climate-element
          id="domain"
          .hass=${0}
          .lcn=${0}
          .softwareSerial=${0}
          @validity-changed=${0}
        ></lcn-config-climate-element>`),this.hass,this.lcn,this._deviceConfig.software_serial,this._validityChanged);case"cover":return(0,r.dy)(be||(be=Ae`<lcn-config-cover-element
          id="domain"
          .hass=${0}
          .lcn=${0}
        ></lcn-config-cover-element>`),this.hass,this.lcn);case"light":return(0,r.dy)($e||($e=Ae`<lcn-config-light-element
          id="domain"
          .hass=${0}
          .lcn=${0}
          @validity-changed=${0}
        ></lcn-config-light-element>`),this.hass,this.lcn,this._validityChanged);case"scene":return(0,r.dy)(Te||(Te=Ae`<lcn-config-scene-element
          id="domain"
          .hass=${0}
          .lcn=${0}
          @validity-changed=${0}
        ></lcn-config-scene-element>`),this.hass,this.lcn,this._validityChanged);case"sensor":return(0,r.dy)(Ce||(Ce=Ae`<lcn-config-sensor-element
          id="domain"
          .hass=${0}
          .lcn=${0}
          .softwareSerial=${0}
        ></lcn-config-sensor-element>`),this.hass,this.lcn,this._deviceConfig.software_serial);case"switch":return(0,r.dy)(xe||(xe=Ae`<lcn-config-switch-element
          id="domain"
          .hass=${0}
          .lcn=${0}
        ></lcn-config-switch-element>`),this.hass,this.lcn);default:return r.Ld}}},{kind:"method",key:"_deviceChanged",value:function(e){const t=e.target,i=(0,$.zD)(t.value);this._deviceConfig=this.deviceConfigs.find((e=>e.address[0]===i[0]&&e.address[1]===i[1]&&e.address[2]===i[2]))}},{kind:"method",key:"_nameChanged",value:function(e){const t=e.target;this._name=t.value,this._validityChanged(new CustomEvent("validity-changed",{detail:!this._name}))}},{kind:"method",key:"_validityChanged",value:function(e){this._invalid=e.detail}},{kind:"method",key:"_create",value:async function(){var e;const t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("#domain"),i={name:this._name?this._name:this.domain,address:this._deviceConfig.address,domain:this.domain,domain_data:t.domainData};await this._params.createEntity(i)?this._closeDialog():await(0,pe.Ys)(this,{title:this.lcn.localize("dashboard-entities-dialog-add-alert-title"),text:`${this.lcn.localize("dashboard-entities-dialog-add-alert-text")}\n              ${this.lcn.localize("dashboard-entities-dialog-add-alert-hint")}`})}},{kind:"method",key:"_closeDialog",value:function(){this._params=void 0,(0,y.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_domainChanged",value:function(e){const t=e.target;this.domain=t.value}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,r.iv)(Re||(Re=Ae`
        ha-dialog {
          --mdc-dialog-max-width: 500px;
          --dialog-z-index: 10;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        #name-input {
          margin-bottom: 25px;
        }
        .buttons {
          display: flex;
          justify-content: space-between;
          padding: 8px;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
      `))]}}]}}),r.oi)}}]);
//# sourceMappingURL=71.94b5c5835c7d8816.js.map