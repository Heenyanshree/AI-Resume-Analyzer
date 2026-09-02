import { useState } from "react";
import "./App.css";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from "recharts";
import {
  FaFileAlt,
  FaFileUpload,
  FaRobot,
  FaChartLine,
  FaCheckCircle,
  FaTimesCircle,
} from "react-icons/fa";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [pages, setPages] = useState(0);
  const [words, setWords] = useState(0);
  const [atsScore, setAtsScore] = useState(0);
  const [missingSkills, setMissingSkills] = useState([]);
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [jd, setJd] = useState("");
  const [matchScore, setMatchScore] = useState(0);
  const [aiData, setAiData] = useState("");
  const [loadingAI, setLoadingAI] = useState(false);
  const [history, setHistory] = useState([]);

  const chartData = [
    { name: "Matched", value: matchedSkills.length },
    { name: "Missing", value: missingSkills.length },
  ];

  const COLORS = ["#22c55e", "#ef4444"];

  // Upload Resume
  const uploadResume = async () => {
    if (!file) {
      alert("Choose a resume first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setText(data.text || "");
      setPages(data.pages || 0);
      setWords(data.words || 0);
      setAtsScore(data.ats_score || 0);
      setMatchedSkills(data.matched_skills || []);
      setMissingSkills(data.missing_skills || []);

      setHistory((prev) => [
        {
          name: file.name,
          ats: data.ats_score,
          pages: data.pages,
          words: data.words,
        },
        ...prev,
      ]);

      alert("Resume analyzed successfully!");
    } catch (error) {
      console.error(error);
      alert("Upload failed!");
    }
  };

  // JD Match
  const matchResume = async () => {
    if (!text || !jd) {
      alert("Upload resume and paste Job Description first!");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: text,
          job_description: jd,
        }),
      });

      const data = await response.json();

      setMatchScore(data.match_score || 0);
      setMatchedSkills(data.matched_skills || []);
      setMissingSkills(data.missing_skills || []);
    } catch (error) {
      console.error(error);
      alert("Matching failed!");
    }
  };

  // AI Suggestions
  const generateSuggestions = async () => {
    if (!text || !jd) {
      alert("Upload resume and paste Job Description first!");
      return;
    }

    setLoadingAI(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload/suggestions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            resume_text: text,
            job_description: jd,
          }),
        }
      );

      const data = await response.json();

      if (data.suggestions?.response) {
        setAiData(data.suggestions.response);
      } else if (data.response) {
        setAiData(data.response);
      } else {
        setAiData("No suggestions found.");
      }
    } catch (error) {
      console.error(error);
      alert("AI Suggestions failed!");
    }

    setLoadingAI(false);
  };

  // Download PDF Report
  const downloadReport = () => {
    const doc = new jsPDF();

    doc.setFontSize(22);
    doc.text("AI Resume Analyzer Report", 20, 20);

    doc.setFontSize(12);
    doc.text(`ATS Score: ${atsScore}/100`, 20, 35);
    doc.text(`JD Match: ${matchScore}%`, 20, 45);
    doc.text(`Pages: ${pages}`, 20, 55);
    doc.text(`Words: ${words}`, 20, 65);

    autoTable(doc, {
      startY: 80,
      head: [["Matched Skills", "Missing Skills"]],
      body: [
        [
          matchedSkills.join(", ") || "None",
          missingSkills.join(", ") || "None",
        ],
      ],
    });

    let y = doc.lastAutoTable.finalY + 15;

    doc.setFontSize(16);
    doc.text("AI Suggestions", 20, y);

    doc.setFontSize(11);

    const split = doc.splitTextToSize(aiData || "No AI Suggestions", 170);

    doc.text(split, 20, y + 10);

    doc.save("AI_Resume_Report.pdf");
  };

  return (
    <>
      {/* Background Glow */}
      <div className="bg-glow"></div>

      {/* Navbar */}
      <nav className="navbar">
        <div className="logo-section">
          <div className="logo-circle">AI</div>

          <div>
            <h2>AI Resume Analyzer</h2>
            <p>Professional ATS Dashboard</p>
          </div>
        </div>

        <button className="profile-btn">Dashboard</button>
      </nav>

      <div className="container">
        {/* Upload */}
        <div className="upload-box glass-card">
          <div className="upload-area">
            <FaFileUpload className="upload-icon" />

            <h3>Drag & Drop Resume</h3>

            <p>Upload your PDF or DOCX Resume</p>

            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>

          <button className="primary-btn" onClick={uploadResume}>
            Analyze Resume
          </button>
        </div>

        {/* Dashboard */}
        <div className="stats">
          <div className="card glass-card hover-card">
            <FaFileAlt className="card-icon" />
            <h2>{pages}</h2>
            <p>Pages</p>
          </div>

          <div className="card glass-card hover-card">
            <FaChartLine className="card-icon" />
            <h2>{words}</h2>
            <p>Words</p>
          </div>

          <div className="card glass-card hover-card green">
            <div className="large-gauge">
              <CircularProgressbar
                value={atsScore}
                text={`${atsScore}%`}
                styles={buildStyles({
                  textColor: "#fff",
                  pathColor: "#22c55e",
                  trailColor: "#1e293b",
                })}
              />
            </div>

            <p>ATS Score</p>
          </div>

          <div className="card glass-card hover-card blue">
            <FaRobot className="card-icon" />
            <h2>{matchScore}%</h2>
            <p>JD Match</p>
          </div>
        </div>

        {/* Progress */}
        <div className="progress-box glass-card">
          <p>ATS Progress • {atsScore}%</p>

          <div className="progress">
            <div
              className="progress-fill"
              style={{ width: `${atsScore}%` }}
            ></div>
          </div>
        </div>

        {/* Skills */}
        <div className="skills-grid">
          <div className="skill-card glass-card">
            <h3>Matched Skills</h3>

            {matchedSkills.length === 0 ? (
              <p className="empty">No matched skills yet.</p>
            ) : (
              <ul className="matched">
                {matchedSkills.map((skill, index) => (
                  <li key={index}>
                    <FaCheckCircle /> {skill}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="skill-card glass-card">
            <h3>Missing Skills</h3>

            {missingSkills.length === 0 ? (
              <p className="empty">No missing skills 🎉</p>
            ) : (
              <ul className="missing">
                {missingSkills.map((skill, index) => (
                  <li key={index}>
                    <FaTimesCircle /> {skill}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* JD Match */}
        <div className="jd-box glass-card">
          <h2>Job Description Match</h2>

          <textarea
            rows="8"
            placeholder="Paste Job Description..."
            value={jd}
            onChange={(e) => setJd(e.target.value)}
          />

          <button className="primary-btn" onClick={matchResume}>
            Compare Resume
          </button>

          <div className="match-result">
            <h2>{matchScore}% Match</h2>
          </div>
        </div>

        {/* AI Suggestions */}
        <div className="ai-card glass-card">
          <h2>AI Resume Suggestions</h2>

          <button className="primary-btn" onClick={generateSuggestions}>
            {loadingAI ? "Generating..." : "Generate AI Suggestions"}
          </button>

          <button className="secondary-btn" onClick={downloadReport}>
            📄 Download PDF Report
          </button>

          {aiData && (
            <div className="ai-output">
              {aiData.split("\n").map(
                (line, index) =>
                  line.trim() && (
                    <div className="ai-line" key={index}>
                      {line}
                    </div>
                  )
              )}
            </div>
          )}
        </div>

        {/* Skills Analytics */}
        <div className="chart-card glass-card">
          <h2>Skills Analytics</h2>

          <div style={{ width: "100%", height: 280 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={90}
                  label
                >
                  {chartData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index]} />
                  ))}
                </Pie>

                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* History */}
        <div className="history-card glass-card">
          <h2>Recent Resume History</h2>

          {history.length === 0 ? (
            <p className="empty">No resumes uploaded.</p>
          ) : (
            history.map((item, index) => (
              <div className="history-item" key={index}>
                <div>
                  <strong>{item.name}</strong>
                  <p>
                    {item.pages} pages • {item.words} words
                  </p>
                </div>

                <div className="history-score">{item.ats}%</div>
              </div>
            ))
          )}
        </div>

        {/* Resume Preview */}
        {text && (
          <div className="preview glass-card">
            <div className="preview-header">📄 Resume Preview</div>

            <pre>{text}</pre>
          </div>
        )}
      </div>
    </>
  );
}

export default App;