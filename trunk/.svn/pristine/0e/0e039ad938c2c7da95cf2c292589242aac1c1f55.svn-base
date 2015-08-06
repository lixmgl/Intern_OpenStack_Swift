/*
 * Copyright (C) 2011 Tildeslash Ltd. All rights reserved.
 */


if ((typeof MMONIT == "undefined") || (! MMONIT)) { var MMONIT = {}; }


/**
 * Declare the MMONIT namespace with common methods, variables and
 * define a few useful prototype functions.
 *
 * @file
 */
 
 
/** 
 * Dom manipulation methods 
 */
MMONIT.dom = function() {
     return {
         /**
         * Get element from DOM
         * @param String/HTMLElement | el : Accepts a string to use as an ID for getting a DOM reference, or an actual DOM reference
         * @return a DOM node
         */
         get: function(el) {
             if (typeof el === 'string') {
                 return document.getElementById(el);
             } else {
                 return el;
             }
         },
         /**
         * Add element to dest
         * @param String/HTMLElement | el : the Node to add
         * @param String/HTMLElement | dest : the target Node to append el to
         */
         add: function(el, dest) {
             var e = this.get(el);
             var d = this.get(dest);
             d.appendChild(e);
         },
         /**
         * Remove el from DOM
         * @param String/HTMLElement | el : the Node to remove
         */
         remove: function(el) {
             var e = this.get(el);
             el.parentNode.removeChild(e);
         },
         /**
         * Find first parent of refNode with nodeName = sName
         * @param HTMLElement | refNode : the DOM Node to start searching from
         * @param String | sName : the nodeName to search for
         */
         findParent: function (refNode, sName) {
             var t = refNode.parentNode;
             while (t) {
                 if (t.nodeName.toLowerCase() == sName.toLowerCase()) break;
                 t = t.parentNode;
             }
             return t;
         }
     };
}();


/** 
 * Layer methods 
 */
MMONIT.layer = function() {
    return {
        /**
         * Toggle element visibility using the display attribute. 
         * Hide element if visible otherwise show element
         * @param String/HTMLElements | varargs : DOM nodes to toogle visibility of
         * @return true if visible otherwise false
         */
         toggle : function() {
             for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                 el.style.display = (el.style.display != 'none' ? 'none' : '' );
             }
             return MMONIT.dom.get(arguments[0]).style.display == '';
         },
        /**
         * Show element using the display attribute
         * @param String/HTMLElements | varargs : DOM nodes to show
         */
        show :  function() {
            for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                el.style.display = '';
            }
        },
        /**
         * Hide element using the display attribute
         * @param variable String/HTMLElements | varargs : DOM nodes to hide
         */
        hide :  function() {
            for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                el.style.display = 'none';
            }
        },
        /**
         * Toggle element visibility using the visibility property. 
         * Hide element if visible otherwise show element
         * @param String/HTMLElements | varargs : DOM nodes to toogle visibility of
         */
        vtoggle : function() {
            for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                el.style.visibility = (el.style.visibility != 'hidden' ? 'hidden' : 'visible' );
            }
        },
        /**
         * Show elements using the visibility property
         * @param String/HTMLElements | varargs : DOM nodes to make visible
         */
        vshow : function() {
            for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                el.style.visibility = 'visible';
            }
        },
        /**
        * Hide elements using the visibility property
        * @param String/HTMLElements | varargs : DOM nodes to hide
         */
        vhide : function() {
            for (var i = 0, el; (el = MMONIT.dom.get(arguments[i])); i++) {
                el.style.visibility = 'hidden';
            }
        }
    };
}();


/** 
 * Listbox methods 
 */
MMONIT.list = function() {
    return {
        /**
         * Sort options attributes in a listbox
         * @param Object | oList : The list to sort
         */
        sort :  function(oList) {
            if (oList.options === null) return;
            var o = new Array();
            for (var i = 0; i < oList.options.length; i++) {
                o[o.length] = new Option( oList.options[i].text, oList.options[i].value, oList.options[i].defaultSelected, oList.options[i].selected) ;
            }
            if (o.length === 0) { return; }
            o = o.sort(function(a,b) { 
                    if ((a.text + "") < (b.text+"")) return -1; if ((a.text + "") > (b.text + "")) return 1; return 0;
            });
            for (var i = 0; i < o.length; i++) {
                oList.options[i] = new Option(o[i].text, o[i].value, o[i].defaultSelected, o[i].selected);
            }
        },
        /**
         * Move selected options attributes between listboxes
         * @param Object | from : The list to move selected options from
         * @param Object | to : The list to move selected options to
         */
        move :  function(from, to) {
            if (from.options !== null) {
                for (var i = 0; i < from.options.length; i++) {
                    var o = from.options[i];
                    if (o.selected) {
                        var index = 0;
                        if (to.options !== null) {
                            index = to.options.length;
                        }
                        to.options[index] = new Option( o.text, o.value, false, false);
                    }
                }
                for (var i = (from.options.length-1); i >= 0; i--) {
                    var o = from.options[i];
                    if (o.selected) {
                        from.options[i] = null;
                    }
                }
                MMONIT.list.sort(from);
                MMONIT.list.sort(to);
                from.selectedIndex = -1;
                to.selectedIndex = -1;
            }
        },
        /**
         * Returns number of selected rows in oList
         * @param Object | oList : The list to find selected rows in
         * @return Number of rows selected in oList
         */
        hasSelected :  function(oList) {
            var s = 0;
            if (oList.options !== null) {
                for (var i = 0; i < oList.options.length; i++)
                    if (oList.options[i].selected) s++;
            }
            return s;
        },
        /**
         * Set sValue as the selected value of oList
         * @param Object | oList : The list to set the selected row
         * @param String | sValue : The selected value to set
         */
        setSelected :  function(oList, sValue) {
            var s = 0;
            if (oList.options) {
                for (var i = 0; i < oList.options.length; i++) {
                    if (oList.options[i].value == sValue) {
                        oList.options[i].selected = true;
                        break;
                    }
                }
            }       
        }

    };
}();


/** 
 * Animation effects. NOTE, clients should include YUI animation 
 */
MMONIT.effects = function() {
    return {
        /**
         * Author: Dustin Diaz, http://www.dustindiaz.com/
         * License http://creativecommons.org/licenses/by-sa/2.5/
         * @param String/HTMLElement | oEl : Accepts a string to use as an ID for getting a DOM reference, or an actual DOM reference
         * @param Int | iOffset : The unit (in 'px') that the element will be shaken 'by'
         * @param Int | iNum : The number of times the motion will iterate
         * @param Int | iSpeed : The speed at which the motion will animate
         */
        shake : function(oEl, iOffset, iNum, iSpeed) {
            var xy = YAHOO.util.Dom.getXY(oEl);
            var left = xy[0]-iOffset;
            var right = xy[0]+iOffset;
            (function(type, args, count) {
                if ( count >= iNum ) {
                    var a = {
                        points : {
                            to : xy
                        }
                    };
                    var anim = new YAHOO.util.Motion(oEl, a, iSpeed);
                    anim.animate();
                    return;
                }
                else if ( count % 2 ) {
                    var c = count+1;
                    var a = {
                        points : {
                            to : [right, xy[1]]
                        }
                    };
                    var anim = new YAHOO.util.Motion(oEl, a, iSpeed);
                    anim.onComplete.subscribe(arguments.callee, c);
                    anim.animate();
                }
                else {
                    var c = count+1;
                    var a = {
                        points : {
                            to : [left, xy[1]]
                        }
                    };
                    var anim = new YAHOO.util.Motion(oEl, a, iSpeed);
                    anim.onComplete.subscribe(arguments.callee, c);
                    anim.animate();
                }
                })(null, null, 1);
        }
    };
}();


MMONIT.datatable = {};
/** 
 * DataTable columns sort factory
 */
MMONIT.datatable.sort = function() {
    return {
        /**
         * Returns a sort function for sorting a datatable column of real values. E.g. percent
         * @param String | field : The datatable column (key) to sort
         * @return A sort function suitable for sorting real values
         */
        compareReal : function(field) {
            return function(a, b, desc) {
                    var r = parseFloat(a.getData(field)) - parseFloat(b.getData(field));
                    return desc ? r * -1 : r;
            };
        }
    };
}();

/** 
 * DataTable search
 * Clients should include YAHOO.util.Dom and YAHOO.util.Event 
 */
MMONIT.datatable.search = function() {
    /**
     * Clients should set this value to true if the DataTable was updated and
     * rows changed to enable persistent search across table refresh
     */
    this.shouldApplyClientSearch = false;
    /**
     * Clients should set this value to true if the DataTable should update
     * its cache before applying the search
     */
    this.shouldRefreshCache = false;
    
    return {
        /**
         * Setup a Client search field for a DataTable. Text entered into the field is 
         * used to filter the table in-memory and only show those rows that match
         * the search criteria. 
         * @param Object | oTable : The DataTable to search
         * @param String | sColumn : The data column to filter/search on
         * @param String | elField : Id of the input text field to use as a search field
         * @param String | sLabel : Label to put into elField when blured
         */
        client: function (oTable, sColumn, elField, sLabel) {
                var myDelayId = -1;
                var myCache = [];
                var mySearchField = MMONIT.dom.get(elField);
                if (mySearchField.value === '') {
                    mySearchField.value = sLabel;
                    YAHOO.util.Dom.setStyle(mySearchField, "color", "#999");
                }
                YAHOO.util.Event.on(mySearchField, "focus", function(e) { 
                    if (mySearchField.value == sLabel) {
                        mySearchField.value = '';
                    }
                    YAHOO.util.Dom.setStyle(mySearchField, "color", "#000");
                }); 
                YAHOO.util.Event.on(mySearchField, "blur", function(e) { 
                    if (mySearchField.value === '') {
                        mySearchField.value = sLabel;
                        YAHOO.util.Dom.setStyle(mySearchField, "color", "#999");
                    }
                }); 
                /* Get and cache the original record-set of oTable. This set is used
                 to reset the table between search to avoid sending a JSON request to
                 reinitialize the table */
                var buildCache = function () {
                    var rs = oTable.getRecordSet();
                    var records = rs.getRecords();
                    for (var i = 0; i < records.length; i++) {
                        myCache[myCache.length] = records[i].getData();
                    }
                }; 
                /* A row was removed from the table. Find the row removed and delete
                 it from myCache to keep the cache in sync. We cannot use 
                 e.recordIndex since the current oTable record-set may be a subset
                 of the cached record-set if a search was performed and the row was
                 removed from the search sub-set */
                oTable.subscribe("rowDeleteEvent", function(e) { 
                    for (var i = 0; i < myCache.length; i++) {
                        if (e.oldData.id == myCache[i].id) {
                            myCache.splice(i, 1);
                            break;
                        }
                    }
                }); 
                /* The DataTable search function; Re-populate table from cache and filter
                out records that does not match the search field text */
                var myTableSearch = function () {
                    if (MMONIT.datatable.search.shouldRefreshCache) {
                        MMONIT.datatable.search.shouldRefreshCache = false;
                        myCache = [];
                    }
                    if (myCache.length === 0) buildCache();
                    MMONIT.datatable.search.shouldApplyClientSearch = false;
                    oTable.getRecordSet().replaceRecords(myCache);
                    var toReplace = [];
                    var rs = oTable.getRecordSet();
                    var records = rs.getRecords();
                    for (var data = null, i = 0; i < records.length; i++) {
                        data = records[i].getData();
                        if (data[sColumn].startsWith(mySearchField.value)) {
                            toReplace[toReplace.length] = data; 
                        }
                    }
                    if (toReplace.length < records.length) {
                        rs.replaceRecords(toReplace);
                    }
                    var paginator = oTable.get('paginator');
                    if (paginator) {
                        paginator.set('totalRecords', toReplace.length);
                    }
                    oTable.render();
                };
                /* If the table was updated from DataSource and rendered while text was entered in
                the search field, run the search function again to make the DataTable re-display the
                search result. That is, make table search persistent across Table refresh. Since the
                postRender Event is also sent when we do the actual search in myTableSearch,
                we must check and set the guard variable, shouldApplyClientSearch, to avoid ending 
                up in a very tight loop. */
                oTable.subscribe("beforeRenderEvent", function(e) {
                    if (! ((! MMONIT.datatable.search.shouldApplyClientSearch) || (mySearchField.value == '') || (mySearchField.value == sLabel))) {
                        MMONIT.datatable.search.shouldApplyClientSearch = false;
                        myTableSearch();
                    }
                }); 
                /* Perform search using a timer to buffer key events. I.e. we 
                 search using all characters entered in the search field within 200 ms */
                YAHOO.util.Event.on(mySearchField, "keyup", function(e) { 
                    if (myDelayId != -1) {
                        myDelayId = -1;
                        clearTimeout(myDelayId);
                    }
                    myDelayId = setTimeout(myTableSearch, (200));
                }); 
        },
        /**
         * Setup a Server search field for a DataTable. Text entered into the field is 
         * used to perform a server-side search and (re)populate the table.
         * @param Object | oTable : The DataTable to search
         * @param String | sColumn : The data column to filter/search on
         * @param String | elField : Id of the input text field to use as a search field
         * @param String | sLabel : Label to put into elField when blured
         */
        server: function (oTable, sColumn, elField, sLabel) {
                var myDelayId = -1;
                var mySearchField = MMONIT.dom.get(elField);
                if (! mySearchField.value) {
                    mySearchField.value = sLabel;
                    YAHOO.util.Dom.setStyle(mySearchField, "color", "#999");
                }
                mySearchField.eventReload = new YAHOO.util.CustomEvent("reload", mySearchField);
                YAHOO.util.Event.on(mySearchField, "focus", function(e) {
                    if (mySearchField.value == sLabel) {
                        mySearchField.value = '';
                    }
                    YAHOO.util.Dom.setStyle(mySearchField, "color", "#000");
                });
                YAHOO.util.Event.on(mySearchField, "blur", function(e) {
                    if (mySearchField.value === '') {
                        mySearchField.value = sLabel;
                        YAHOO.util.Dom.setStyle(mySearchField, "color", "#999");
                    }
                });
                /* Perform search using a timer to buffer key events. I.e. we 
                 search on all characters entered in the search field within 400 ms */
                YAHOO.util.Event.on(mySearchField, "keyup", function(e) {
                    if (myDelayId != -1) {
                        clearTimeout(myDelayId);
                    }
                    myDelayId = -1;
                    myDelayId = setTimeout(function () {
                        var oCallback = {
                            success : function(o) {
                                          oTable.getDataSource().sendRequest('.', { 
                                              success  : oTable.onDataReturnInitializeTable,
                                              scope    : oTable,
                                              argument : oTable.getState() });
                                          mySearchField.eventReload.fire();
                                      },
                            failure : function(o) {
                                          alert(o.responseText);
                                      },
                            timeout: 5000
                        };
                        var sUrl = ".?" + elField + "=" + mySearchField.value;
                        YAHOO.util.Connect.asyncRequest('GET', sUrl, oCallback);
                    }, (400));
                });
        }
    };
}();


/** 
 * Synchronous AJAX (SJAX) 
 */
MMONIT.sjax = function() {
    return {
        /**
         * Performs a SJAX POST request
         * @param String | url : The url to send a POST request
         * @param String | postData : Data to be sent in entity body
         * @return response text
         */
         post: function (url, postData) {
             var http = null;
             if (window.XMLHttpRequest) {              
                 http = new XMLHttpRequest();              
             } else {                                  
                 http = new ActiveXObject("Microsoft.XMLHTTP");
             }
             if (http) {
                 http.open("POST", url, false);
                 http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                 http.send(postData);
                 return http.responseText;                                         
             } else {
                 return "null";
             }                                             
         }
    };
}();


/**
 * Returns a new URL within the M/Monit server by appending the given relativeURL to
 * the current location. If the current location does not contain an ending slash it
 * is added before the relativeURL is appended.
 * @param String | relativeURL : The relative url to append to the current location
 * @return The new M/Monit URL suitable for assigning to window.location.
 */
MMONIT.location = function(relativeURL) {
     var s = window.location.href.split('?')[0];
     if (s.charAt(s.length-1) != '/') {
         s += '/';
     }
     return s + relativeURL;
};


/* ------------------------------------------------------------ Prototypes */


/**
 * A String trim function available to all String objects 
 */
String.prototype.trim = function() {
    return this.replace(/^(\s*)|(\s*)$/g,'');
};


/**
 * Returns true if String starts with str
 */
String.prototype.startsWith = function(str) {
    return (this.indexOf(str) === 0);
};


/**
 * Return String truncated at n and with a trailing ellipsis. 
 */
String.prototype.trunc = function(n) {
    return this.length > n ? this.substr(0, n-1) + '...' : this;
};


/**
 * Test for membership operator available to all Array objects
 */
Array.prototype.contains = function(el) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == el) {
            return true;
        }
    }
    return false;
};

