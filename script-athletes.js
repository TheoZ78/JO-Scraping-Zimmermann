fetch('athletes.json')
  .then(response => response.json())
  .then(data => {
    const athletes = data.map(a => {
      let gold = 0, silver = 0, bronze = 0;
      if (Array.isArray(a.palmares)) {
        a.palmares.forEach(medal => {
          if (medal.medal === "gold") gold++;
          if (medal.medal === "silver") silver++;
          if (medal.medal === "bronze") bronze++;
        });
      }
      return {
        name: (a.first_name || "") + " " + (a.last_name || ""),
        gold,
        silver,
        bronze,
        total: gold + silver + bronze
      };
    });
    const top = athletes
      .filter(a => a.total > 0)
      .sort((a, b) => b.total - a.total)
      .slice(0, 20);

    const categories = top.map(a => a.name);
    const goldData = top.map(a => a.gold);
    const silverData = top.map(a => a.silver);
    const bronzeData = top.map(a => a.bronze);

    Highcharts.chart('chart-athletes', {
      chart: { type: 'column', height: 500 },
      title: { text: 'Top 20 des athlètes les plus médaillés' },
      xAxis: {
        categories,
        title: { text: 'Athlètes' }
      },
      yAxis: {
        min: 0,
        title: { text: 'Nombre de médailles' },
        allowDecimals: false,
        stackLabels: { enabled: true }
      },
      legend: { reversed: true },
      tooltip: {
        shared: true,
        headerFormat: '',
        formatter: function () {
          let total = 0;
          this.points.forEach(pt => { total += pt.y; });
          const pos = this.points[0].point.index + 1;
          const nom = this.points[0].key;
          return `<b>#${pos} - ${nom}</b><br/>Total médailles : <b>${total}</b>`;
        }
      },
      plotOptions: {
        column: { stacking: 'normal', dataLabels: { enabled: true } }
      },
      series: [
        { name: 'Or', data: goldData, color: '#FFD700' },
        { name: 'Argent', data: silverData, color: '#C0C0C0' },
        { name: 'Bronze', data: bronzeData, color: '#CD7F32' }
      ]
    });
  });
