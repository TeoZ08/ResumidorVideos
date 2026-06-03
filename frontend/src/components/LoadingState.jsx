import { useEffect, useState } from "react";

const STEPS = ["Validando link", "Buscando legenda", "Gerando resumo"];

export default function LoadingState({ active }) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!active) {
      setStep(0);
      return undefined;
    }

    const interval = window.setInterval(() => {
      setStep((current) => Math.min(current + 1, STEPS.length - 1));
    }, 2200);

    return () => window.clearInterval(interval);
  }, [active]);

  if (!active) {
    return null;
  }

  return (
    <div className="loading-state">
      <span className="loader" />
      <span>{STEPS[step]}</span>
    </div>
  );
}
