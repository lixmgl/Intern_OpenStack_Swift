/*
 * Copyright (C) 2011 Tildeslash Ltd. All rights reserved.
 */


/**
 * This Report module is used in both reports/ and reports/host/ to drive
 * the GUI. Synthesized into a common module as the GUI is more or less 
 * identical for the two reports. The little difference there is, is handled
 * by aReportConfig object given as an argument to this module's start method. 
 */
var Report = function () {
    return {
        /**
         * Start the Report GUI
         * @param object | aReportConfig : Config object to handle the difference
         * between the host report and service report
         */
        start:function(aReportConfig) {
            var Dom = YAHOO.util.Dom; 
            /* Get JSON data and build UI */
            var myDataSource = new YAHOO.util.XHRDataSource(aReportConfig.datasource);
            myDataSource.connMethodPost = true;
            myDataSource.connXhrMode = "cancelStaleRequests";
            myDataSource.responseType = YAHOO.util.XHRDataSource.TYPE_JSON;
            myDataSource.responseSchema = {
                resultsList: "items",
                fields: [{key: "id"}, {key: "active"}, {key: "name"}, {key: "uptime"}, {key: "downtime"}, {key: "events", parser: "number"}], 
                metaFields : {Range : "Range", DateFrom : "DateFrom", DateTo : "DateTo", Uptime : "Uptime", Downtime : "Downtime"}
            };
            /* Datatable Formatter: Grey out inactive hosts/services */
            var myNameFormatter = function(elCell, oRecord, oColumn, oData) {
                elCell.innerHTML = oRecord.getData("name");
                if (! parseInt(oRecord.getData("active")))
                    Dom.addClass(this.getTrEl(elCell),"light-grey-text");
            };
            /* Datatable */
            var myColumnDefs = [
                {key:"name",label:aReportConfig.columnLabel, sortable:true, formatter:myNameFormatter},
                {key:"uptime", label:"Uptime", sortable:true, sortOptions:{sortFunction:MMONIT.datatable.sort.compareReal("uptime")}},
                {key:"downtime", label:"Downtime", sortable:false},
                {key:"events", label:"Events", sortable:true, formatter:aReportConfig.eventsLinkFormatter}
            ];
            var myConfig = {
                selectionMode:"single",
                sortedBy : {key: "uptime", dir: YAHOO.widget.DataTable.CLASS_ASC},
                paginator : new YAHOO.widget.Paginator({
                    alwaysVisible: false,
                    rowsPerPage    : aReportConfig.rowsperpage,
                    rowsPerPageOptions : [15, 60, 100, 500],
                    template       : '<input class="search-field toright" type="text" id="searchField" size="15">' + "{PageLinks} {RowsPerPageDropdown}"
                })
            };
            var myDataTable = new YAHOO.widget.DataTable("mytable", myColumnDefs, myDataSource, myConfig);
            if (aReportConfig.rowsclickable) {
                myDataTable.subscribe("rowMouseoverEvent", myDataTable.onEventHighlightRow);
                myDataTable.subscribe("rowMouseoutEvent", myDataTable.onEventUnhighlightRow);
                myDataTable.subscribe("rowClickEvent", function(e) {
                    window.location = MMONIT.location('host/' + myDataTable.getRecord(e.target).getData("id"));
                }); 
            }
            myDataTable.doBeforeLoadData = function(sRequest, oResponse, oPayload) {
                if (oResponse.error)
                    myDataTable.showTableMessage("Load error: " + oResponse.statusText);
                MMONIT.layer.vhide("spinner");
                var r = oResponse.meta;
                aReportConfig.dateFrom = r.DateFrom;
                aReportConfig.dateTo = r.DateTo;
                var df = new Date(aReportConfig.dateFrom * 1000);
                var dt = new Date(aReportConfig.dateTo * 1000);
                Dom.get("range-value").innerHTML = df.getFullYear() + '-' + (df.getMonth() + 1) + '-' + df.getDate() + ' - ' + dt.getFullYear() + '-' + (dt.getMonth() + 1) + '-' + dt.getDate();
                Dom.get("Uptime").innerHTML = r.Uptime;
                Dom.get("Downtime").innerHTML = r.Downtime;
                oResponse.results.sort(function(a,b) {return parseFloat(a.uptime) - parseFloat(b.uptime);});
                myDataTable.set("sortedBy", {key: "uptime", dir: YAHOO.widget.DataTable.CLASS_ASC});
                // "Notify" that DataTable search should re-run and refresh cache
                MMONIT.datatable.search.shouldApplyClientSearch = true;
                MMONIT.datatable.search.shouldRefreshCache = true;
                // Update slider
                var range = r.Range * 40;
                mySlider.setValue(range, true, false, true); // Don't fire events to prevent slideEnd handler to fire again and initialize another request
                Dom.setStyle(mySliderHighlight,'width', range + 'px'); 
                return true;
            };
            myConfig.paginator.subscribe('render', function(e) {
                /* If the top paginator is displayed; Setup the datatable search field defined inside the paginator container
                and make the paginator always visible to avoid having the paginator and search field disappear if table size change on search */
                if (this.getContainerNodes()[0].style.display == '') {
                    MMONIT.datatable.search.client(myDataTable, 'name', 'searchField', aReportConfig.searchLabel);
                    this.set('alwaysVisible', true);
                }
            });
            myConfig.paginator.subscribe('rowsPerPageChange', function(e) {
                // Make paginator rows per page changes persistent by saving value in session
                if (e.newValue != e.prevValue)
                    YAHOO.util.Connect.asyncRequest('POST', aReportConfig.homepath + 'json/session/put', {}, 'Report_Rows='+e.newValue);
            });
            /* Range slider */
            var mySlider = YAHOO.widget.Slider.getHorizSlider("slider-background", "slider-thumb", 0, 240, 40);
            var mySliderHighlight = Dom.get("slider-background-blue");
            mySlider.subscribe('change', function (offset) {
                Dom.setStyle(mySliderHighlight,'width', offset + 'px'); 
            });
            mySlider.subscribe("slideEnd", function() {
                var range = mySlider.getValue() / 40;
                // Show a spinner if processing takes more than 0.3 sec
                var t = setTimeout("MMONIT.layer.vshow('spinner')", 300);
                mySlider.lock(); // Lock slider while processing request
                myDataTable.getDataSource().sendRequest("range=" + range, { 
                    success : function(oRequest, oResponse, oPayload) {
                                clearTimeout(t);
                                mySlider.unlock();
                                myDataTable.onDataReturnReplaceRows(oRequest, oResponse, oPayload);
                            },
                    failure : function(oRequest, oResponse, oPayload) { 
                                clearTimeout(t);
                                mySlider.unlock();
                                alert("Update error. HTTP status code ["+oResponse.status +"]");
                            }
                });
            });
        }
    };
}();
    
    
