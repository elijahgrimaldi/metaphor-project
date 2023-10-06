import React, { useState } from 'react';
import { Pie } from 'react-chartjs-2';
import './App.css';
import { Chart, ArcElement, CategoryScale, PieController } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';


Chart.register(ArcElement, CategoryScale, PieController, ChartDataLabels);

function App() {
    const [result, setResult] = useState(null);
    const [stockSymbol, setStockSymbol] = useState('');
    const [sentimentCounts, setSentimentCounts] = useState(null);

    const handleExecute = async (symbol) => {
        const response = await fetch('http://127.0.0.1:5000/stock_analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol
            })
        });

        const data = await response.json();
        setResult(data.result.overall_sentiment);
        setSentimentCounts(data.result.sentiment_counts);
    };

    const data = {
        labels: ['POSITIVE', 'NEGATIVE', 'NEUTRAL'],
        datasets: [
            {
                data: [sentimentCounts?.POSITIVE, sentimentCounts?.NEGATIVE, sentimentCounts?.NEUTRAL],
                backgroundColor: ['#4CAF50', '#FF5733', '#FFC300']
            }
        ]
    };

    const options = {
      plugins: {
        tooltip: {
          callbacks: {
            title: function(tooltipItem) {
              return ''; // Removing the title
            },
            label: function(tooltipItem, data) {
              const label = data.labels[tooltipItem.dataIndex];
              return label + ': ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.dataIndex];
            }
          }
        },
        datalabels: {
          color: 'white',
          formatter: function(value, context) {
            return context.chart.data.labels[context.dataIndex];
          },
        }
      }
    };
    
  

    return (
        <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '50px' }}>
            <h1>Stock Sentiment Analysis</h1>
            <div style={{ width: '300px', marginBottom: '20px' }}>
                <input 
                    type="text" 
                    placeholder="Enter Stock Symbol" 
                    value={stockSymbol} 
                    onChange={e => setStockSymbol(e.target.value)}
                    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
                />
            </div>
            <button onClick={() => handleExecute(stockSymbol)} style={{ padding: '10px 20px', borderRadius: '5px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}>
                Submit
            </button>
            {result && <div style={{ marginTop: '20px', padding: '10px', borderRadius: '5px', background: '#f7f7f7', border: '1px solid #e7e7e7' }}>Result: {result}</div>}
            {sentimentCounts && (
                <div style={{ marginTop: '20px', width: '300px', height: '300px' }}>
                  <Pie data={data} key={stockSymbol} options={options} plugins={[ChartDataLabels]} />
                </div>
            )}
            <footer style={{ marginTop: '50px', fontSize: '12px' }}>
                Powered by Metaphor API
            </footer>
        </div>
    );
}

export default App;
