import { useState, useRef, useEffect } from 'react';

const QA = [
  {
    category: '📊 Overview',
    items: [
      { q: 'What is CanAI Café?', a: 'CanAI Café is a data intelligence platform that analyzes café transaction data across 8 Canadian provinces. We process raw sales data through an automated pipeline and visualize insights for decision-makers.' },
      { q: 'How much revenue did we generate?', a: 'Total revenue for 2023 was approximately $86,311 across 8,435 transactions, with an average transaction value of $10.23.' },
      { q: 'What are our top products?', a: 'Sandwich leads with ~$20.7K in revenue (24%), followed by Coffee at ~$19.3K (22.4%), and Salad at ~$13.5K (15.7%). Food items drive the highest revenue per transaction.' },
      { q: 'Which provinces perform best?', a: 'Ontario is the largest market, followed by British Columbia and Quebec. Together they account for over 60% of total revenue.' },
    ]
  },
  {
    category: '⚙️ Pipeline',
    items: [
      { q: 'How does the data pipeline work?', a: 'The pipeline has 3 stages: (1) dataset_cleaner.py cleans raw Excel data, (2) dataset_profiler.py generates quality metrics, (3) generate_dashboard_data.py produces 13 JSON files that power the React dashboard.' },
      { q: 'What is the data quality score?', a: 'After cleaning, our data quality score is 97.6%. The pipeline handles missing values, standardizes formats, removes duplicates, and validates all entries automatically.' },
      { q: 'What tools and tech do we use?', a: 'Python (pandas, numpy, openpyxl) for data processing, React + Vite for the frontend, Recharts for visualizations, and the entire pipeline is automated via run_all.py.' },
    ]
  },
  {
    category: '💡 Insights',
    items: [
      { q: 'What payment methods are used?', a: 'Credit Card is the most popular payment method, followed by Debit and Cash. Mobile Pay is growing but still the smallest segment — an opportunity for targeted promotions.' },
      { q: 'Weekday vs weekend sales?', a: 'Weekday transactions are higher in volume, but weekends show a higher average transaction value. Customers tend to spend more per visit on weekends.' },
      { q: 'Any recommendations?', a: 'Key recommendations: (1) Expand sandwich and food combos — highest revenue items, (2) Boost mobile payment adoption with discounts, (3) Run weekend promotions to capitalize on higher spend, (4) Focus marketing on underperforming provinces.' },
    ]
  },
  {
    category: '🚀 Future Plans',
    items: [
      { q: 'What AI features are planned?', a: 'We plan to integrate a trained AI model that provides real-time conversational analytics, predictive forecasting with ML, anomaly detection for unusual sales patterns, and natural language querying of the dataset.' },
      { q: 'What\'s on the roadmap?', a: 'Next steps include: live data streaming from POS systems, Power BI embedded reports, customer segmentation with clustering, and a mobile companion app for managers on the go.' },
    ]
  },
  {
    category: '😄 Fun',
    items: [
      { q: 'What do CanAI people do after Friday?', a: 'They espresso themselves all weekend! ☕ But honestly, our data shows weekend transactions have a higher average spend — so even the team can\'t resist treating themselves to an extra latte on Saturday.' },
    ]
  }
];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [showQuestions, setShowQuestions] = useState(true);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleQuestion = (item) => {
    setMessages(prev => [
      ...prev,
      { role: 'user', text: item.q },
      { role: 'assistant', text: item.a }
    ]);
    setShowQuestions(false);
    setTimeout(() => setShowQuestions(true), 300);
  };

  const handleClear = () => {
    setMessages([]);
    setShowQuestions(true);
  };

  return (
    <>
      <style>{`
        .chat-fab {
          position: fixed;
          bottom: 24px;
          right: 24px;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: linear-gradient(135deg, #5b341f, #c7923e);
          border: none;
          color: white;
          font-size: 28px;
          cursor: pointer;
          box-shadow: 0 6px 20px rgba(91, 52, 31, 0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.2s, box-shadow 0.2s;
          z-index: 1000;
        }
        .chat-fab:hover {
          transform: scale(1.1);
          box-shadow: 0 8px 28px rgba(91, 52, 31, 0.5);
        }
        .chat-panel {
          position: fixed;
          bottom: 96px;
          right: 24px;
          width: 400px;
          height: 540px;
          background: #fff;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(44, 24, 16, 0.25);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          z-index: 1000;
          animation: chatSlideUp 0.3s ease;
        }
        @keyframes chatSlideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .chat-header {
          background: linear-gradient(135deg, #5b341f, #2c1810);
          color: white;
          padding: 16px 20px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .chat-header-left h3 {
          margin: 0;
          font-size: 15px;
          font-weight: 700;
        }
        .chat-header-left p {
          margin: 2px 0 0;
          font-size: 11px;
          opacity: 0.65;
        }
        .chat-header-actions {
          display: flex;
          gap: 8px;
        }
        .chat-header-btn {
          background: rgba(255,255,255,0.15);
          border: none;
          color: white;
          font-size: 13px;
          cursor: pointer;
          border-radius: 6px;
          padding: 4px 8px;
          transition: background 0.2s;
        }
        .chat-header-btn:hover { background: rgba(255,255,255,0.25); }
        .chat-body {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 10px;
          background: #f9f6f2;
        }
        .chat-welcome {
          text-align: center;
          padding: 10px 0 6px;
          color: #2c1810;
        }
        .chat-welcome .chat-avatar {
          font-size: 36px;
          margin-bottom: 6px;
        }
        .chat-welcome h4 {
          margin: 0;
          font-size: 14px;
          font-weight: 700;
        }
        .chat-welcome p {
          margin: 4px 0 0;
          font-size: 12px;
          color: #667085;
        }
        .chat-category {
          font-size: 11px;
          font-weight: 700;
          color: #5b341f;
          margin: 8px 0 4px;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .chat-q-btn {
          display: block;
          width: 100%;
          text-align: left;
          background: white;
          border: 1px solid #e5ded5;
          border-radius: 12px;
          padding: 10px 14px;
          font-size: 13px;
          color: #2c1810;
          cursor: pointer;
          transition: all 0.15s;
          line-height: 1.4;
        }
        .chat-q-btn:hover {
          background: #5b341f;
          color: white;
          border-color: #5b341f;
          transform: translateX(4px);
        }
        .chat-msg {
          max-width: 88%;
          padding: 10px 14px;
          border-radius: 14px;
          font-size: 13px;
          line-height: 1.55;
          word-wrap: break-word;
        }
        .chat-msg.user {
          align-self: flex-end;
          background: #5b341f;
          color: white;
          border-bottom-right-radius: 4px;
        }
        .chat-msg.assistant {
          align-self: flex-start;
          background: white;
          color: #2c1810;
          border: 1px solid #e5ded5;
          border-bottom-left-radius: 4px;
        }
        .chat-footer {
          padding: 12px 16px;
          border-top: 1px solid #e5ded5;
          background: white;
          text-align: center;
          font-size: 11px;
          color: #667085;
        }
      `}</style>

      <button className="chat-fab" onClick={() => setOpen(!open)} title="CanAI Assistant">
        {open ? '✕' : '🤖'}
      </button>

      {open && (
        <div className="chat-panel">
          <div className="chat-header">
            <div className="chat-header-left">
              <h3>🤖 CanAI Café Assistant</h3>
              <p>Ask me about the café data</p>
            </div>
            <div className="chat-header-actions">
              {messages.length > 0 && (
                <button className="chat-header-btn" onClick={handleClear} title="Clear chat">🗑️</button>
              )}
              <button className="chat-header-btn" onClick={() => setOpen(false)}>✕</button>
            </div>
          </div>

          <div className="chat-body">
            <div className="chat-welcome">
              <div className="chat-avatar">🤖</div>
              <h4>Hi! I'm your CanAI Café Assistant</h4>
              <p>Tap a question below to get started</p>
            </div>

            {messages.map((msg, i) => (
              <div key={i} className={`chat-msg ${msg.role}`}>{msg.text}</div>
            ))}

            {showQuestions && (
              <>
                {QA.map(cat => (
                  <div key={cat.category}>
                    <div className="chat-category">{cat.category}</div>
                    {cat.items.map(item => (
                      <button key={item.q} className="chat-q-btn" onClick={() => handleQuestion(item)}>
                        {item.q}
                      </button>
                    ))}
                  </div>
                ))}
              </>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="chat-footer">
            Powered by CanAI Intelligence Engine
          </div>
        </div>
      )}
    </>
  );
}
