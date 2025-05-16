fetch('sports.json')
  .then(res => res.json())
  .then(data => {
    const countryMedals = {};
    data.forEach(sportObj => {
      const sport = sportObj.sport;
      sportObj.medals_by_country.forEach(countryObj => {
        const country = countryObj.country;
        const total = (countryObj.gold || 0) + (countryObj.silver || 0) + (countryObj.bronze || 0);
        if (!countryMedals[country]) countryMedals[country] = {};
        countryMedals[country][sport] = total;
      });
    });
    const sportTotals = {}, countryTotals = {};
    for (const country in countryMedals) {
      countryTotals[country] = 0;
      for (const sport in countryMedals[country]) {
        countryTotals[country] += countryMedals[country][sport];
        sportTotals[sport] = (sportTotals[sport] || 0) + countryMedals[country][sport];
      }
    }
    const topCountries = Object.entries(countryTotals)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10).map(([name]) => name);
    const topSports = Object.entries(sportTotals)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10).map(([name]) => name);

    const heatmapData = [];
    topCountries.forEach((country, i) => {
      topSports.forEach((sport, j) => {
        heatmapData.push([j, i, countryMedals[country][sport] || 0]);
      });
    });

    Highcharts.chart('chart-heatmap', {
      chart: { type: 'heatmap', height: 500 },
      title: { text: 'Heatmap des médailles par sport et pays' },
      xAxis: { categories: topSports, title: { text: "Sport" } },
      yAxis: { categories: topCountries, title: { text: "Pays" }, reversed: true },
      colorAxis: { min: 0, stops: [[0, '#e6f7ff'], [0.5, '#1890ff'], [1, '#001529']] },
      legend: { align: 'right', layout: 'vertical', verticalAlign: 'middle' },
      tooltip: {
        formatter: function() {
          return `<b>Pays:</b> ${this.series.yAxis.categories[this.point.y]}<br>
                  <b>Sport:</b> ${this.series.xAxis.categories[this.point.x]}<br>
                  <b>Médailles:</b> ${this.point.value}`;
        }
      },
      series: [{
        name: "Nombre de médailles",
        borderWidth: 1,
        data: heatmapData,
        dataLabels: { enabled: true, color: '#000' }
      }]
    });
  });
