import React from "react";
import { FiUploadCloud, FiCpu, FiCheckCircle } from "react-icons/fi";

interface Section {
  name: string;
  score: number;
  strength: string;
  suggestion: string;
}

interface Props {
  sections: Section[];
}

const ResumeSectionBreakdown: React.FC<Props> = ({ sections }) => {
  return (
    <div className="section-breakdown">
      <h3>📋 Resume Section-wise Breakdown</h3>

      {sections.map((section) => (
        <div key={section.name} className="section-card">
          <div className="section-header">
            <span>{section.name}</span>
            <span>{section.score}%</span>
          </div>

          <div className="progress">
            <div
              className="progress-fill"
              style={{ width: `${section.score}%` }}
            />
          </div>

          <p>
            <strong>Strength:</strong> {section.strength}
          </p>

          <p>
            <strong>Suggestion:</strong> {section.suggestion}
          </p>
        </div>
      ))}
    </div>
  );
};

export default ResumeSectionBreakdown;