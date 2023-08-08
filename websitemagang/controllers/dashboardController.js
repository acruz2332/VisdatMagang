const processed_data = require("../models/processed_data");


//dashboard with all datas
const dashboardView = (req, res) => {
  const data = processed_data.find({} , (err, data) => {
    if (err){
      console.log(err);
    }else{
      //counting sum of data by the sources
      let count_detik = data.filter(item => item.sumber === 'detik');
      let count_kompas = data.filter(item => item.sumber === 'kompas');

      //get filter label for each source
      const label_detik = [...new Set(count_detik.map(item => item.label))];
      const label_kompas = [...new Set(count_kompas.map(item => item.label))];

      //get count label by diff source (detik)
      nightingale_detik_data = []
      label_detik.forEach((item, index) => {
        nightingale_detik_data.push({"name": item, "value": (count_detik.filter(itemm => itemm.label === item)).length });
      })

      //get count label by diff source (kompas)
      nightingale_kompas_data = []
      label_kompas.forEach((item, index) => {
        nightingale_kompas_data.push({"name": item, "value": (count_kompas.filter(itemm => itemm.label === item)).length})
      })

      //=============================================DETIK=============================================================
      //date as X
      detik_published_date = []
      count_detik.forEach((item, index) => {
        detik_published_date.push(item.published_date)
      })
      detik_published_date = Array.from(new Set(detik_published_date));

      //netral from detik
      const netral_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Netral';
      });
      //positif from detik
      const positif_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Positif';
      });
      //negatif from detik
      const negatif_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Negatif';
      });

      //start cutting netral detik
      dates_of_detik_netral = ['Netral']
      detik_published_date.forEach((item, index) => {
        const a = netral_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_netral.push(a.length);
      })

      //start cutting positif detik
      dates_of_detik_positif = ['Positif']
      detik_published_date.forEach((item, index) => {
        const a = positif_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_positif.push(a.length);
      })

      //start cutting negatif detik
      dates_of_detik_negatif = ['Negatif']
      detik_published_date.forEach((item, index) => {
        const a = negatif_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_negatif.push(a.length);
      })

      for (var i = 0; i < detik_published_date.length; i++){
        detik_published_date[i] = detik_published_date[i].slice(-2);
      }
      detik_published_date.unshift("Date"); //ini nanti

      //===============================================================================================================

      //=============================================KOMPAS=============================================================
      //date as X
      kompas_published_date = []
      count_kompas.forEach((item, index) => {
        kompas_published_date.push(item.published_date)
      })
      kompas_published_date = Array.from(new Set(kompas_published_date));

      //netral from kompas
      const netral_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Netral';
      });
      //positif from kompas
      const positif_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Positif';
      });
      //negatif from kompas
      const negatif_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Negatif';
      });

      //start cutting netral kompas
      dates_of_kompas_netral = ['Netral']
      kompas_published_date.forEach((item, index) => {
        const a = netral_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_netral.push(a.length);
      })

      //start cutting positif kompas
      dates_of_kompas_positif = ['Positif']
      kompas_published_date.forEach((item, index) => {
        const a = positif_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_positif.push(a.length);
      })

      //start cutting negatif kompas
      dates_of_kompas_negatif = ['Negatif']
      kompas_published_date.forEach((item, index) => {
        const a = negatif_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_negatif.push(a.length);
      })

      for (var i = 0; i < kompas_published_date.length; i++){
        kompas_published_date[i] = kompas_published_date[i].slice(-2);
      }
      kompas_published_date.unshift("Date"); //ini nanti

      //===============================================================================================================
      //=============================================================BAR SENTIMEN======================================
      const total_data = [count_detik.length, count_kompas.length];
      const total_netral = [netral_detik.length, netral_kompas.length];
      const total_positif = [positif_detik.length, positif_kompas.length];
      const total_negatif = [negatif_detik.length, negatif_detik.length]

      const chartData = { bar: 
      [
        { name: 'Detik', value: count_detik.length },
        { name: 'Kompas', value: count_kompas.length },
      ],
        nightingale_detik: nightingale_detik_data,
        nightingale_kompas: nightingale_kompas_data,
        linepie_detik: [detik_published_date, dates_of_detik_netral, dates_of_detik_positif, dates_of_detik_negatif],
        linepie_kompas: [kompas_published_date, dates_of_kompas_netral, dates_of_kompas_positif, dates_of_kompas_negatif],
        bar_sentimen: {total : total_data, netral: total_netral, positif: total_positif, negatif: total_negatif}
    };

    res.render("dashboard", {chartData});
    
    }
  })
};

const dashboardViewStartEnd = (req, res) => {
  const startDate = req.body.start;
  const endDate = req.body.end;
  
  const data = processed_data.find({published_date: {$gte: startDate, $lte: endDate}} , (err, data) => {
    if (err){
      console.log(err);
    }else{
      //counting sum of data by the sources
      const count_detik = data.filter(item => item.sumber === 'detik');
      const count_kompas = data.filter(item => item.sumber === 'kompas');

      //get filter label for each source
      const label_detik = [...new Set(count_detik.map(item => item.label))];
      const label_kompas = [...new Set(count_kompas.map(item => item.label))];

      //get count label by diff source (detik)
      nightingale_detik_data = []
      label_detik.forEach((item, index) => {
        nightingale_detik_data.push({"name": item, "value": (count_detik.filter(itemm => itemm.label === item)).length });
      })

      //get count label by diff source (kompas)
      nightingale_kompas_data = []
      label_kompas.forEach((item, index) => {
        nightingale_kompas_data.push({"name": item, "value": (count_kompas.filter(itemm => itemm.label === item)).length})
      })

      //=============================================DETIK=============================================================
      //date as X
      detik_published_date = []
      count_detik.forEach((item, index) => {
        detik_published_date.push(item.published_date)
      })
      detik_published_date = Array.from(new Set(detik_published_date));

      //netral from detik
      const netral_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Netral';
      });
      //positif from detik
      const positif_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Positif';
      });
      //negatif from detik
      const negatif_detik = data.filter(function(item) {
        return item.sumber === 'detik' && item.sentimen == 'Negatif';
      });

      //start cutting netral detik
      dates_of_detik_netral = ['Netral']
      detik_published_date.forEach((item, index) => {
        const a = netral_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_netral.push(a.length);
      })

      //start cutting positif detik
      dates_of_detik_positif = ['Positif']
      detik_published_date.forEach((item, index) => {
        const a = positif_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_positif.push(a.length);
      })

      //start cutting negatif detik
      dates_of_detik_negatif = ['Negatif']
      detik_published_date.forEach((item, index) => {
        const a = negatif_detik.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_detik_negatif.push(a.length);
      })

      for (var i = 0; i < detik_published_date.length; i++){
        detik_published_date[i] = detik_published_date[i].slice(-2);
      }
      detik_published_date.unshift("Date"); //ini nanti

      //===============================================================================================================
      //=============================================KOMPAS=============================================================
      //date as X
      kompas_published_date = []
      count_kompas.forEach((item, index) => {
        kompas_published_date.push(item.published_date)
      })
      kompas_published_date = Array.from(new Set(kompas_published_date));

      //netral from kompas
      const netral_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Netral';
      });
      //positif from kompas
      const positif_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Positif';
      });
      //negatif from kompas
      const negatif_kompas = data.filter(function(item) {
        return item.sumber === 'kompas' && item.sentimen == 'Negatif';
      });

      //start cutting netral kompas
      dates_of_kompas_netral = ['Netral']
      kompas_published_date.forEach((item, index) => {
        const a = netral_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_netral.push(a.length);
      })

      //start cutting positif kompas
      dates_of_kompas_positif = ['Positif']
      kompas_published_date.forEach((item, index) => {
        const a = positif_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_positif.push(a.length);
      })

      //start cutting negatif kompas
      dates_of_kompas_negatif = ['Negatif']
      kompas_published_date.forEach((item, index) => {
        const a = negatif_kompas.filter(function(itx) {
          return itx.published_date === item;
        })
        dates_of_kompas_negatif.push(a.length);
      })

      for (var i = 0; i < kompas_published_date.length; i++){
        kompas_published_date[i] = kompas_published_date[i].slice(-2);
      }
      kompas_published_date.unshift("Date"); //ini nanti

      //===============================================================================================================
       //=============================================================BAR SENTIMEN======================================
       const total_data = [count_detik.length, count_kompas.length];
       const total_netral = [netral_detik.length, netral_kompas.length];
       const total_positif = [positif_detik.length, positif_kompas.length];
       const total_negatif = [negatif_detik.length, negatif_detik.length]
      

      const chartData = { bar: 
      [
        { name: 'Detik', value: count_detik.length },
        { name: 'Kompas', value: count_kompas.length },
      ],
        nightingale_detik: nightingale_detik_data,
        nightingale_kompas: nightingale_kompas_data,
        linepie_detik: [detik_published_date, dates_of_detik_netral, dates_of_detik_positif, dates_of_detik_negatif],
        linepie_kompas: [kompas_published_date, dates_of_kompas_netral, dates_of_kompas_positif, dates_of_kompas_negatif],
        bar_sentimen: {total : total_data, netral: total_netral, positif: total_positif, negatif: total_negatif}
    };

    res.render("dashboard", {chartData});

    }
  })
};


module.exports = {
  dashboardView,
  dashboardViewStartEnd
};
