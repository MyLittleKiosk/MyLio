import type { ChartOptions } from 'chart.js';
import { ArcElement, Chart as ChartJS, Legend, Title, Tooltip } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const config = (): ChartOptions<'pie'> => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      align: 'center',
      labels: {
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 10,
        font: {
          size: 14,
        },
      },
    },
  },
});

export { config };
