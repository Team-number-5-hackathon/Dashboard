<<<<<<< HEAD
import React from 'react';
=======
import React, { useEffect, useRef } from 'react';
>>>>>>> front-dev
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const ChartLeftBars = ({ data }) => {
<<<<<<< HEAD
=======
    const chartRef = useRef(null);

    useEffect(() => {
        const chart = chartRef.current;

        if (chart) {
            chart.data.labels = data.map(item => item.skill_name);
            chart.data.datasets[0].data = data.map(item => item.average_rating || item.skill_level);
            chart.update();
        }
    }, [data]);

>>>>>>> front-dev
    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }

    const options = {
        indexAxis: 'y',
        elements: {
            bar: {
                borderWidth: 2,
                borderRadius: 12,
            },
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: false,
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                max: 5,
                ticks: {
                    stepSize: 1,
                },
            },
            y: {
                position: 'right',
                ticks: {
<<<<<<< HEAD
=======
                    callback: function(value, index) {
                        return this.getLabelForValue(value);
                    },
>>>>>>> front-dev
                    font: {
                        size: 11,
                    },
                },
                grid: {
                    display: false,
                },
            },
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
            },
        },
        barThickness: 32,
    };

    const chartData = {
        labels: data.map(item => item.skill_name),
        datasets: [
            {
<<<<<<< HEAD
                data: data.map(item => item.average_rating || item.skill_level),
=======
                data: data.map(item => item.average_rating),
>>>>>>> front-dev
                backgroundColor: 'rgba(255, 218, 124, 0.6)',
                borderColor: 'rgb(255, 218, 124)',
                borderWidth: 1,
            },
        ],
    };

    const plugins = [{
        id: 'customPlugin',
        afterDraw: (chart) => {
            const ctx = chart.ctx;
            const xAxis = chart.scales.x;
            const yAxis = chart.scales.y;

            chart.data.datasets.forEach((dataset, i) => {
                const meta = chart.getDatasetMeta(i);
                if (!meta.hidden) {
                    meta.data.forEach((bar, index) => {
                        const data = dataset.data[index];
                        if (data !== undefined && data !== null) {
                            const formattedData = Number(data).toFixed(2);
                            const xValue = xAxis.getPixelForValue(data);
                            const yValue = yAxis.getPixelForValue(chart.data.labels[index]);

                            ctx.fillStyle = 'black';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.font = '10px Arial';
<<<<<<< HEAD
=======
                            ctx.fontWeight = '100';
>>>>>>> front-dev
                            ctx.fillText(formattedData, xValue - 20, yValue);
                        }
                    });
                }
            });
        }
    }];

    return (
        <div style={{ height: `${data.length * 40}px`, width: '100%' }}>
<<<<<<< HEAD
            <Bar options={options} data={chartData} plugins={plugins} />
=======
            <Bar ref={chartRef} options={options} data={chartData} plugins={plugins} />
>>>>>>> front-dev
        </div>
    );
};

<<<<<<< HEAD
export default ChartLeftBars;
=======
export default ChartLeftBars;
>>>>>>> front-dev
