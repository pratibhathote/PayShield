import { useState } from "react";
import {
  ShieldCheck,
  CreditCard,
  MessageSquareWarning,
  AlertTriangle,
  CheckCircle2,
  Activity,
} from "lucide-react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [transaction, setTransaction] = useState({
    amount: "",
    hour: 12,
    new_beneficiary: 0,
    device_changed: 0,
    location_changed: 0,
    transactions_today: 1,
    amount_deviation: 1,
    beneficiary_age_days: 30,
    is_weekend: 0,
  });

  const [message, setMessage] = useState("");
  const [transactionResult, setTransactionResult] = useState(null);
  const [messageResult, setMessageResult] = useState(null);

  const [loadingTransaction, setLoadingTransaction] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState(false);

  const [error, setError] = useState("");

  const updateTransaction = (field, value) => {
    setTransaction((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const analyzeTransaction = async () => {
    if (!transaction.amount) {
      setError("Please enter a transaction amount.");
      return;
    }

    setLoadingTransaction(true);
    setError("");

    try {
      const payload = {
        ...transaction,
        amount: Number(transaction.amount),
        hour: Number(transaction.hour),
        new_beneficiary: Number(transaction.new_beneficiary),
        device_changed: Number(transaction.device_changed),
        location_changed: Number(transaction.location_changed),
        transactions_today: Number(transaction.transactions_today),
        amount_deviation: Number(transaction.amount_deviation),
        beneficiary_age_days: Number(transaction.beneficiary_age_days),
        is_weekend: Number(transaction.is_weekend),
      };

      const response = await fetch(`${API_URL}/analyze/transaction`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Transaction analysis failed.");
      }

      const data = await response.json();
      setTransactionResult(data);
    } catch (err) {
      setError(
        "Could not connect to PayShield API. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoadingTransaction(false);
    }
  };

  const analyzeMessage = async () => {
    if (!message.trim()) {
      setError("Please enter a message to analyze.");
      return;
    }

    setLoadingMessage(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/analyze/message`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
        }),
      });

      if (!response.ok) {
        throw new Error("Message analysis failed.");
      }

      const data = await response.json();
      setMessageResult(data);
    } catch (err) {
      setError(
        "Could not connect to PayShield API. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoadingMessage(false);
    }
  };

  const riskClass = (level) => {
    if (level === "HIGH") return "risk-high";
    if (level === "MEDIUM") return "risk-medium";
    return "risk-low";
  };

  return (
    <div className="app">
      {/* NAVBAR */}
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <ShieldCheck size={24} />
          </div>

          <div>
            <h1>PayShield</h1>
            <p>Pre-Payment Risk & Scam Analyzer</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Risk Engine Online
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="container">

        {/* HERO SECTION */}
        <section className="hero">
          <div className="hero-badge">
            <Activity size={15} />
            AI-ASSISTED PAYMENT SECURITY
          </div>

          <h2>
            Think before you <span>pay.</span>
          </h2>

          <p>
            Analyze suspicious transaction behavior and payment messages
            before taking action.
          </p>
        </section>

        {/* ERROR MESSAGE */}
        {error && <div className="error-box">{error}</div>}

        {/* ANALYZERS */}
        <section className="dashboard-grid">

          {/* TRANSACTION ANALYZER */}
          <div className="card">

            <div className="card-header">
              <div className="card-icon">
                <CreditCard size={21} />
              </div>

              <div>
                <h3>Transaction Risk</h3>
                <p>Analyze payment behavior</p>
              </div>
            </div>

            <div className="form-grid">

              <div className="field full">
                <label>Transaction Amount</label>

                <div className="input-prefix">
                  <span>₹</span>

                  <input
                    type="number"
                    placeholder="e.g. 18500"
                    value={transaction.amount}
                    onChange={(e) =>
                      updateTransaction("amount", e.target.value)
                    }
                  />
                </div>
              </div>

              <div className="field">
                <label>Transaction Hour</label>

                <input
                  type="number"
                  min="0"
                  max="23"
                  value={transaction.hour}
                  onChange={(e) =>
                    updateTransaction("hour", e.target.value)
                  }
                />
              </div>

              <div className="field">
                <label>Transactions Today</label>

                <input
                  type="number"
                  min="1"
                  value={transaction.transactions_today}
                  onChange={(e) =>
                    updateTransaction(
                      "transactions_today",
                      e.target.value
                    )
                  }
                />
              </div>

              <div className="field">
                <label>Amount Deviation</label>

                <input
                  type="number"
                  step="0.1"
                  value={transaction.amount_deviation}
                  onChange={(e) =>
                    updateTransaction(
                      "amount_deviation",
                      e.target.value
                    )
                  }
                />
              </div>

              <div className="field">
                <label>Beneficiary Age (days)</label>

                <input
                  type="number"
                  min="0"
                  value={transaction.beneficiary_age_days}
                  onChange={(e) =>
                    updateTransaction(
                      "beneficiary_age_days",
                      e.target.value
                    )
                  }
                />
              </div>

            </div>

            {/* TOGGLES */}
            <div className="toggle-grid">

              {[
                ["new_beneficiary", "New Beneficiary"],
                ["device_changed", "Device Changed"],
                ["location_changed", "Location Changed"],
                ["is_weekend", "Weekend"],
              ].map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  className={`toggle ${
                    transaction[key] ? "active" : ""
                  }`}
                  onClick={() =>
                    updateTransaction(
                      key,
                      transaction[key] ? 0 : 1
                    )
                  }
                >
                  <span className="toggle-circle"></span>
                  {label}
                </button>
              ))}

            </div>

            <button
              className="primary-btn"
              onClick={analyzeTransaction}
              disabled={loadingTransaction}
            >
              {loadingTransaction
                ? "Analyzing..."
                : "Analyze Transaction"}
            </button>

            {/* TRANSACTION RESULT */}
            {transactionResult && (
              <div className="result">

                <div className="result-top">

                  <div>
                    <span className="result-label">
                      RISK SCORE
                    </span>

                    <strong>
                      {transactionResult.risk_score}/100
                    </strong>
                  </div>

                  <span
                    className={`risk-badge ${riskClass(
                      transactionResult.risk_level
                    )}`}
                  >
                    {transactionResult.risk_level}
                  </span>

                </div>

                <div className="result-section">

                  <h4>
                    <AlertTriangle size={16} />
                    Risk Factors
                  </h4>

                  {transactionResult.reasons?.map(
                    (reason, index) => (
                      <div
                        className="reason"
                        key={index}
                      >
                        <span>•</span>
                        {reason}
                      </div>
                    )
                  )}

                </div>

                <div className="recommendation">

                  <CheckCircle2 size={18} />

                  <div>
                    <strong>Recommended Action</strong>

                    <p>
                      {transactionResult.recommendation}
                    </p>
                  </div>

                </div>

              </div>
            )}

          </div>

          {/* SCAM MESSAGE ANALYZER */}
          <div className="card">

            <div className="card-header">

              <div className="card-icon purple">
                <MessageSquareWarning size={21} />
              </div>

              <div>
                <h3>Scam Message</h3>
                <p>Detect suspicious message patterns</p>
              </div>

            </div>

            <div className="field">

              <label>Payment Message</label>

              <textarea
                placeholder="Paste a suspicious SMS, WhatsApp message, email or payment request..."
                value={message}
                onChange={(e) =>
                  setMessage(e.target.value)
                }
              />

            </div>

            <button
              className="primary-btn"
              onClick={analyzeMessage}
              disabled={loadingMessage}
            >
              {loadingMessage
                ? "Analyzing..."
                : "Analyze Message"}
            </button>

            {/* MESSAGE RESULT */}
            {messageResult && (
              <div className="result">

                <div className="result-top">

                  <div>
                    <span className="result-label">
                      SCAM RISK
                    </span>

                    <strong>
                      {messageResult.risk_score}/100
                    </strong>
                  </div>

                  <span
                    className={`risk-badge ${riskClass(
                      messageResult.risk_level
                    )}`}
                  >
                    {messageResult.risk_level}
                  </span>

                </div>

                <div className="result-section">

                  <h4>
                    <AlertTriangle size={16} />
                    Detected Indicators
                  </h4>

                  {messageResult.indicators?.map(
                    (indicator, index) => (
                      <div
                        className="reason"
                        key={index}
                      >
                        <span>•</span>
                        {indicator}
                      </div>
                    )
                  )}

                </div>

                <div className="recommendation">

                  <CheckCircle2 size={18} />

                  <div>
                    <strong>Recommended Action</strong>

                    <p>
                      {messageResult.recommendation}
                    </p>
                  </div>

                </div>

              </div>
            )}

          </div>

        </section>

        <footer>
          PayShield is an educational prototype using synthetic data.
          It is not intended for real financial decisions.
        </footer>

      </main>
    </div>
  );
}

export default App;