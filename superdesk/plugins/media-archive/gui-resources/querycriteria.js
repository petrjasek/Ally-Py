var querycriteria = {
    
    formContent : '',
    container : '',
    init : function(params) {
        this.formContent = '';
        this.startLoading();
        this.container = params[0];
    },
    
    addField : function(criteria) {
        this.formContent += criteria.Name + '<input type="text" name="'+ criteria.Key +'"/>' + criteria.Criteria + '<br/>'
    },
    
    returnInputs : function(){
        this.formContent += '<br /><input type="submit" value="submit" /> <input type="reset" value="reset" />';
        $('#'+this.container).append(this.formContent);
    },
    
    startLoading : function() {
        var self = this;
        $.ajax({
            url: 'http://localhost:8080/resources/Superdesk/Archive/QueryCriteria/',
            success: function(data){
                var criterialist = data.QueryCriteriaList;
                for (var i=0; i < criterialist.length; i++) {
                    var criteria = criterialist[i];
                    self.addField(criteria);
                }
                self.returnInputs();
            }
        });
    }
}

