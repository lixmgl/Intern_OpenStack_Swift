/*******************************************************************   
 *        Copyright (c) 2009-2012 Cisco Systems, Inc.
 *        All rights reserved.   
 *        
 * @fileoverview 
 * The xwt.widget.form.IconButton 
 * This widget extends dijit.form.Button with new templatefile 
 * 
 * The purpose of this button widget is to let the button icon have a background image when the mouse hover
 * _onMouse() method is overwritten. 
 * 
 * In this widget's instantiation state, it needs three input parameters: iconClass, iconClassHover, iconClassPressed.
 * 
 * 
 * 
 * @author Jeff Hu jefhu@cisco.com
 * 
 * 2012-03-07 Eric Rumer erumer@cisco.com -
 * 
 * Changed _onMouse code to correctly handle all state changes
 * Changed postCreate to set the iconClass to iconClassDisabled if the button is disabled at creation
 */

dojo.provide("xwt.widget.form.IconButton");
dojo.require("xwt.widget.i18nMixin");
dojo.require("dijit.form.Button");
dojo.require("dijit.Tooltip");

dojo.declare("xwt.widget.form.IconButton",  [dijit.form.Button], {
	// summary::
	//The purpose of this button widget is to let the icon have a background image when the mouse hover
	// _onMouse() method is overwritten. 
	
	
	templateString:null,
	
	templatePath: dojo.moduleUrl("xwt", "widget/templates/form/IconButton.html"),
	
	
	//internal property
	iconClassHover:"",
	
	//internal property  - "dijitEditorIcon dijitEditorIconCopy"
	iconClassPressed:"",
	
	//internal property  - "dijitEditorIcon dijitEditorIconPaste"
	iconClassNormal:"",
	
	//internal property  
	iconClassDisabled:"",
	
	//tooltipText property. String
	tooltipText:"",
	
	iconText:"",
	
	altText:"",
	
	iconTextLookup:"",
	
	altTextLookup:"",
	
	// private blank.gif for a11y
	_blankGif : dojo.moduleUrl("xwt", "themes/reboot2/images/blank.gif"),
	
	// i18nPackageName: String
	//		To support I18N messages. By default, the value is "xwt". Modify based on your requirements.
    i18nPackageName: "",
    
    // i18nBundlerName: String
    //		To support I18N messages. By default, the value is "XMPProperties". Modify based on your requirements.
    i18nBundleName: "",
	
	postMixInProperties : function() {
		this.inherited(arguments);
		this.attributeMap.iconText = {
			node : "iconTextNode",
			type : "innerHTML"
		};
		this.attributeMap.altText = {
			node : "iconNode",
			type : "attribute",
			attribute : "alt"
		};

		var i18mixin = new xwt.widget.i18nMixin();
		if (this.i18nPackageName && this.i18nBundleName) {
			i18mixin.addBundle(this.i18nPackageName, this.i18nBundleName);
			this._messages = dojo.mixin(this._messages, i18mixin._messages);
			this._useI18 = true;
		} else {
			this._useI18 = false;
		}
		if (this._messages) {			
			if (this.iconTextLookup) {
				this.iconText = this._messages[this.iconTextLookup];
			}
			if (this.altTextLookup) {
				this.altText = this._messages[this.altTextLookup];
			}

		}
	},

	
	
	_onMouse : function(/*Event*/ event){	
		// summary:
		//	Overwrite the parent's method to handle special mouse events,
		//	using a different iconClass for each of the three states: hover, pressed, normal.
		
		this.inherited(arguments);
		
		if(!this.disabled){
			switch(event.type){
			    case "mouseenter"://add mouseenter for IE
				case "mouseover":
					// prevent hover state if button is currently pressed
					if (!this._mouseDown){
						// set class to hover
                        if (this.iconClassHover.length>0){
                            this.attr("iconClass", this.iconClassHover);
                        }
                    }
					if (this.tooltipText.length>0){
						var tp = new dijit.Tooltip({connectId: [this.is], label: this.tooltipText });							
					}
					break;
				case "mouseout":
				case "mouseleave":
				   if (this.iconClassNormal.length>0){
					   this.attr("iconClass", this.iconClassNormal);
				   }
				   break;
				case "mousedown" :
					if (this.iconClassPressed.length>0){
						this.attr("iconClass", this.iconClassPressed);
					}
					var mouseUpConnector = this.connect(dojo.body(), "onmouseup", function(){
						if(this._mouseDown && this.isFocusable()){
							this.focus();
						}
						this._active = false;
						this._mouseDown = false;
						if(this._hovering && this.iconClassHover.length>0){
							this.attr("iconClass", this.iconClassHover);
						} else {
							if (this.iconClassNormal.length>0){
								this.attr("iconClass", this.iconClassNormal);
							}
						}
						this._setStateClass();
						this.disconnect(mouseUpConnector);
					});
					break;
			}
		}
		else {
			if (this.iconClassDisabled.length>0){
				this.attr("iconClass", this.iconClassDisabled);
			}
		}
		this._setStateClass();
	},
		
	postCreate : function(){
	// summary::
	//	Widget life-cycle function. 
	//	Captures the input iconClass into the iconClassNormal variable.
	
		//console.log("postCreate");
		this.iconClassNormal = this.iconClass;
		//console.log(" this iconClassNormal " + this.iconClassNormal + " iconClass: " + this.iconClass);
		this.attr("altText",this.altText);	
		this.attr("iconText",this.iconText);
		
		dojo.setSelectable(this.focusNode, false);
		
		if (this.disabled && this.iconClassDisabled.length>0){
			this.attr("iconClass", this.iconClassDisabled);
			this._setStateClass();
		}
		this.inherited(arguments);
	},
	
	setDisabled : function(/*Boolean*/disabled) {
	// summary::
	// 	Enable or disable this button based on a boolean input.
	// disabled: Boolean
	//	True sets the button to disabled state; false enables it.
		this.attr('disabled', disabled);
		if (disabled) {
			if (this.iconClassDisabled.length>0){
				this.attr("iconClass", this.iconClassDisabled);
			}
		}
		else {
			if (this.iconClassNormal.length>0) {
			   this.attr("iconClass", this.iconClassNormal);
			}
		}
		this._setStateClass();
	}	
});