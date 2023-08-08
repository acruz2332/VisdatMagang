const processed_data = require("../models/processed_data");


const DatasView = (req, res) => {

    const data = processed_data.find({} , (err, data) => {
        if (err){
          console.log(err);
        }else{
          const AllDatas = data;
        res.render("data", {AllDatas});
    }
}
)
};


const DatasViewFilter = (req, res) => {

    const data = processed_data.find({} , (err, data) => {

        const sumber = req.body.sumber;
        const sentimen = req.body.sentimen;
        const label = req.body.label;

        if (err){
          console.log(err);
        }else{
            let AllDatas = null;
            
            if (sumber != undefined && sentimen != undefined && label != undefined){
                AllDatas = data.filter(function(item) {
                    return item.sumber == sumber && item.sentimen == sentimen && item.label == label;
                });
            }else if (sumber != undefined && sentimen != undefined){
                AllDatas = data.filter(function(item) {
                    return item.sumber === sumber && item.sentimen == sentimen;
                });
            }else if (sumber != undefined && label != undefined){
                AllDatas = data.filter(function(item) {
                    return item.sumber === sumber && item.label == label;
                });
            }else if (sumber != undefined){
                AllDatas = data.filter(function(item) {
                    return item.sumber === sumber;
                });
            }else if (sentimen != undefined){
                AllDatas = data.filter(function(item) {
                    return item.sentimen == sentimen;
                });
            }else{
                AllDatas = data;
            }

        res.render("data", {AllDatas});
    }
}
)
};
module.exports ={
    DatasView,
    DatasViewFilter
}