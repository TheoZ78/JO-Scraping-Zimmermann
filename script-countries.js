fetch('nations.json')
  .then(res => res.json())
  .then(data => {
    data.sort((a, b) => (b.gold + b.silver + b.bronze) - (a.gold + a.silver + a.bronze));
    const top = data.slice(0, 20);
    const categories = top.map(c => c.country);
    const gold = top.map(c => c.gold);
    const silver = top.map(c => c.silver);
    const bronze = top.map(c => c.bronze);

    Highcharts.chart('chart-countries', {
      chart: { type: 'bar', height: 500 },
      title: { text: 'Classement des pays par médailles' },
      xAxis: { categories, title: { text: 'Pays' } },
      yAxis: {
        min: 1,
        title: { text: 'Nombre de médailles' }
      },
      tooltip: {
        shared: true,
        headerFormat: '',
        formatter: function () {
          let total = 0;
          this.points.forEach(pt => { total += pt.y; });
          return `<b>${this.points[0].key}</b><br/>Total médailles : <b>${total}</b>`;
        }
      },
      plotOptions: {
        series: { stacking: 'normal', dataLabels: { enabled: true } }
      },
      series: [
        { name: 'Or', data: gold, color: '#FFD700' },
        { name: 'Argent', data: silver, color: '#C0C0C0' },
        { name: 'Bronze', data: bronze, color: '#CD7F32' }
      ]
    });
  });
