/**
 * Created by IntelliJ IDEA.
 * User: oleg
 * Date: Sep 23, 2010
 * Time: 9:03:05 AM
 * To change this template use File | Settings | File Templates.
 */

/*!
 * Ext JS Library 3.2.1
 * Copyright(c) 2006-2010 Ext JS, Inc.
 * licensing@extjs.com
 * http://www.extjs.com/license
 */
Ext.onReady(function(){
    Ext.QuickTips.init();

    var Person = Ext.data.Record.create([{
        name: 'name',
        type: 'string'
    }, {
        name: 'birthday',
        type: 'date',
        dateFormat: 'n/j/Y'
    },{
        name: 'age',
        type: 'int'
    },{
        name: 'days',
        type: 'int'
    }]);


    // hideous function to generate employee data
    var genData = function(){
        var data = [];
        var s = new Date(2007, 0, 1);
        var now = new Date(), i = -1;
        while(s.getTime() < now.getTime()){
            var ecount = Ext.ux.getRandomInt(0, 3);
            for(var i = 0; i < ecount; i++){
                var name = Ext.ux.generateName();
                data.push({
                    birthday : s.clearTime(true).add(Date.DAY, Ext.ux.getRandomInt(0, 27)),
                    name : name,
                    days: Math.floor(Ext.ux.getRandomInt(35000, 85000)/1000)*1000
                });
            }
            s = s.add(Date.MONTH, 1);
        }
        return data;
    }


    var store = new Ext.data.GroupingStore({
        reader: new Ext.data.JsonReader({fields: Person}),
//        data: genData(),
        url: '/json_list/',
        autoLoad: true,
        sortInfo: {field: 'days', direction: 'ASC'}
    });

    var editor = new Ext.ux.grid.RowEditor({
        saveText: 'Update'
    });

    var grid = new Ext.grid.GridPanel({
        store: store,
        width: 600,
        region:'center',
        margins: '0 5 5 5',
        autoExpandColumn: 'name',
        plugins: [editor],
        view: new Ext.grid.GroupingView({
            markDirty: false
        }),
        tbar: [{
            iconCls: 'icon-user-add',
            text: 'Add Person',
            handler: function(){
                var e = new Person({
                    name: 'New Guy',
                    birthday: (new Date()).clearTime()
                });
                editor.stopEditing();
                store.insert(0, e);
                grid.getView().refresh();
                grid.getSelectionModel().selectRow(0);
                editor.startEditing(0);
            }
        },{
            ref: '../removeBtn',
            iconCls: 'icon-user-delete',
            text: 'Remove Person',
            disabled: true,
            handler: function(){
                editor.stopEditing();
                var s = grid.getSelectionModel().getSelections();
                for(var i = 0, r; r = s[i]; i++){
                    store.remove(r);
                }
            }
        }],

        columns: [
        new Ext.grid.RowNumberer(),
        {
            id: 'name',
            header: ' Name',
            dataIndex: 'name',
            width: 320,
            sortable: true,
            editor: {
                xtype: 'textfield',
                allowBlank: false
            }
        },{
            xtype: 'datecolumn',
            header: 'Birthday',
            dataIndex: 'birthday',
            format: 'D, jS F, Y',
            width: 200,
            sortable: true,
            groupRenderer: Ext.util.Format.dateRenderer('M y'),
            editor: {
                xtype: 'datefield',
                allowBlank: true,
                minValue: '01/01/1320',
                minText: 'Can\'t have a start date before the company existed!',
                maxValue: (new Date()).format('m/d/Y')
            }
        },{
            xtype: 'numbercolumn',
            header: 'Age',
            dataIndex: 'age',
            format: '0,0',
            width: 100,
            sortable: true,
            editable: false,
            editor: {
                xtype: 'numberfield',
                allowBlank: true
//                minValue: 1,
//                maxValue: 150000
            }
        },{
            xtype: 'numbercolumn',
            header: 'Days',
            dataIndex: 'days',
            format: '0,0',
            width: 100,
            sortable: true,
                editable: false,
            editor: {
                xtype: 'numberfield',
                allowBlank: true
//                minValue: 1,
//                maxValue: 150000
            }
        }]
    });

    var cstore = new Ext.data.JsonStore({
        fields:['month', 'employees', 'salary'],
        data:[],
        refreshData: function(){
            var o = {}, data = [];
            var s = new Date(2007, 0, 1);
            var now = new Date(), i = -1;
            while(s.getTime() < now.getTime()){
                var m = {
                    birthday: s.format('M y'),
                    employees: 0,
                    salary: 0,
                    index: ++i
                }
                data.push(m);
                o[m.month] = m;
                s = s.add(Date.MONTH, 1);
            }
            store.each(function(r){
                var m = o[r.data.birthday.format('M y')];
                for(var i = m.index, mo; mo = data[i]; i++){
                    mo.employees += 10000;
                    mo.salary += r.data.salary;
                }
            });
            this.loadData(data);
        }
    });
//    cstore.refreshData();
//    store.on('add', cstore.refreshData, cstore);
//    store.on('remove', cstore.refreshData, cstore);
//    store.on('update', cstore.refreshData, cstore);

    var layout = new Ext.Panel({
//        title: 'Employee Salary by Month',
        layout: 'border',
        layoutConfig: {
            columns: 1
        },
        width:600,
        height: 400,
        items: [grid]
    });
//    layout.render(Ext.getBody());
    layout.render("list_container");

    grid.getSelectionModel().on('selectionchange', function(sm){
        grid.removeBtn.setDisabled(sm.getCount() < 1);
    });
});
