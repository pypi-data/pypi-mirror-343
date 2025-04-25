"use strict";(self.webpackChunklcn_frontend=self.webpackChunklcn_frontend||[]).push([["626"],{61631:function(e,i,t){var a=t(73577),d=(t(71695),t(47021),t(5601)),s=t(81577),n=t(57243),l=t(50778);let o,r=e=>e;(0,a.Z)([(0,l.Mo)("ha-radio")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[s.W,(0,n.iv)(o||(o=r`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `))]}}]}}),d.J)},59283:function(e,i,t){t.r(i),t.d(i,{CreateDeviceDialog:function(){return m}});var a=t(73577),d=t(72621),s=(t(71695),t(40251),t(11740),t(47021),t(59897),t(61631),t(52158),t(70596),t(11297)),n=t(57243),l=t(50778),o=t(44118),r=t(66193),c=t(42229);let u,h,v=e=>e,m=(0,a.Z)([(0,l.Mo)("lcn-create-device-dialog")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_isGroup",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_segmentId",value(){return 0}},{kind:"field",decorators:[(0,l.SB)()],key:"_addressId",value(){return 5}},{kind:"field",decorators:[(0,l.SB)()],key:"_invalid",value(){return!1}},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this.lcn=e.lcn,await this.updateComplete}},{kind:"method",key:"firstUpdated",value:function(e){(0,d.Z)(t,"firstUpdated",this,3)([e]),(0,c.z)()}},{kind:"method",key:"willUpdate",value:function(e){e.has("_invalid")&&(this._invalid=!this._validateSegmentId(this._segmentId)||!this._validateAddressId(this._addressId,this._isGroup))}},{kind:"method",key:"render",value:function(){return this._params?(0,n.dy)(u||(u=v`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        .heading=${0}
        @closed=${0}
      >
        <div id="type">${0}</div>

        <ha-formfield label=${0}>
          <ha-radio
            name="is_group"
            value="module"
            .checked=${0}
            @change=${0}
          ></ha-radio>
        </ha-formfield>

        <ha-formfield label=${0}>
          <ha-radio
            name="is_group"
            value="group"
            .checked=${0}
            @change=${0}
          ></ha-radio>
        </ha-formfield>

        <ha-textfield
          .label=${0}
          type="number"
          .value=${0}
          min="0"
          required
          autoValidate
          @input=${0}
          .validityTransform=${0}
          .validationMessage=${0}
        ></ha-textfield>

        <ha-textfield
          .label=${0}
          type="number"
          .value=${0}
          min="0"
          required
          autoValidate
          @input=${0}
          .validityTransform=${0}
          .validationMessage=${0}
        ></ha-textfield>

        <div class="buttons">
          <mwc-button
            slot="secondaryAction"
            @click=${0}
            .label=${0}
          ></mwc-button>

          <mwc-button
            slot="primaryAction"
            @click=${0}
            .disabled=${0}
            .label=${0}
          ></mwc-button>
        </div>
      </ha-dialog>
    `),(0,o.i)(this.hass,this.lcn.localize("dashboard-devices-dialog-create-title")),this._closeDialog,this.lcn.localize("type"),this.lcn.localize("module"),!1===this._isGroup,this._isGroupChanged,this.lcn.localize("group"),!0===this._isGroup,this._isGroupChanged,this.lcn.localize("segment-id"),this._segmentId.toString(),this._segmentIdChanged,this._validityTransformSegmentId,this.lcn.localize("dashboard-devices-dialog-error-segment"),this.lcn.localize("id"),this._addressId.toString(),this._addressIdChanged,this._validityTransformAddressId,this._isGroup?this.lcn.localize("dashboard-devices-dialog-error-group"):this.lcn.localize("dashboard-devices-dialog-error-module"),this._closeDialog,this.lcn.localize("dismiss"),this._create,this._invalid,this.lcn.localize("create")):n.Ld}},{kind:"method",key:"_isGroupChanged",value:function(e){this._isGroup="group"===e.target.value}},{kind:"method",key:"_segmentIdChanged",value:function(e){const i=e.target;this._segmentId=+i.value}},{kind:"method",key:"_addressIdChanged",value:function(e){const i=e.target;this._addressId=+i.value}},{kind:"method",key:"_validateSegmentId",value:function(e){return 0===e||e>=5&&e<=128}},{kind:"method",key:"_validateAddressId",value:function(e,i){return e>=5&&e<=254}},{kind:"get",key:"_validityTransformSegmentId",value:function(){return e=>({valid:this._validateSegmentId(+e)})}},{kind:"get",key:"_validityTransformAddressId",value:function(){return e=>({valid:this._validateAddressId(+e,this._isGroup)})}},{kind:"method",key:"_create",value:async function(){const e={name:"",address:[this._segmentId,this._addressId,this._isGroup]};await this._params.createDevice(e),this._closeDialog()}},{kind:"method",key:"_closeDialog",value:function(){this._params=void 0,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,(0,n.iv)(h||(h=v`
        #port-type {
          margin-top: 16px;
        }
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        .buttons {
          display: flex;
          justify-content: space-between;
          padding: 8px;
        }
      `))]}}]}}),n.oi)}}]);
//# sourceMappingURL=lcn-create-device-dialog.7b51c8a3ffe9ad5f.js.map