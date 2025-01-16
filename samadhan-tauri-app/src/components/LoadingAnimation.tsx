import React, { useEffect } from "react";
import { motion, useAnimationControls } from "framer-motion";

export const LoadingAnimation = ({ onComplete }: { onComplete: () => void }) => {
  const controls = useAnimationControls();
  const letterControls = useAnimationControls(); // Controls for the letter expansion animation

  useEffect(() => {
    const animate = async () => {
      // Wave animation for "S"
      await controls.start({
        opacity: [0, 1],
        scale: [0.9, 1],
        transition: { duration: 0.8, ease: "easeOut" },
      });

      await controls.start({
        height: ["0%", "100%"],
        transition: { duration: 3, ease: "easeInOut" },
      });

      // Modified movement animation for the "S"
      controls.start({
        x: -190, // Changed from -80 to -65 to move S slightly right
        scale: 0.4,
        transition: { duration: 0.8, ease: "easeInOut" },
      });

      // Trigger the letter expansion animation after the wave animation completes
      await letterControls.start((i) => ({
        opacity: 1,
        x: 0,
        transition: { delay: i * 0.1, duration: 0.5, ease: "easeOut" },
      }));

      onComplete();
    };

    animate();
  }, [controls, letterControls, onComplete]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#fafafa]">
      <div className="relative" style={{ width: "600px" }}>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={controls}
          className="relative flex items-center justify-center"
          style={{ width: "500px", height: "400px" }}
        >
          <svg width="500" height="400" className="absolute">
            <defs>
              <mask id="s-mask">
                <text
                  x="60%"
                  y="50%"
                  dominantBaseline="middle"
                  textAnchor="middle"
                  className="letter-s text-[280px] font-medium"
                  fill="white"
                >
                  S
                </text>
              </mask>

              <linearGradient id="fluid-gradient" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#6D28D9" />
                <stop offset="100%" stopColor="#7C3AED" />
              </linearGradient>

              <filter id="shadow-effect">
                <feDropShadow dx="0" dy="4" stdDeviation="8" floodOpacity="0.15" />
                <feDropShadow dx="0" dy="8" stdDeviation="12" floodOpacity="0.1" />
              </filter>
            </defs>

            <text
              x="60%"
              y="50%"
              dominantBaseline="middle"
              textAnchor="middle"
              className="letter-s text-[280px] font-medium"
              fill="white"
              filter="url(#shadow-effect)"
            >
              S
            </text>

            <g mask="url(#s-mask)">
              <motion.rect
                x="0"
                y="0"
                width="500"
                height="400"
                fill="url(#fluid-gradient)"
                initial={{ height: "0%" }}
                animate={controls}
                className="fluid-fill"
              />

              <motion.div
                initial={{ y: 400 }}
                animate={{
                  y: 0,
                  transition: { duration: 3, ease: "easeInOut" },
                }}
              >
                <circle
                  className="wave wave-1"
                  cx="150"
                  cy="0"
                  r="200"
                  fill="url(#fluid-gradient)"
                  style={{ opacity: 0.7 }}
                />
                <circle
                  className="wave wave-2"
                  cx="150"
                  cy="0"
                  r="200"
                  fill="url(#fluid-gradient)"
                  style={{ opacity: 0.3 }}
                />
              </motion.div>
            </g>
          </svg>
        </motion.div>

        {/* Updated letter expansion animation */}
        <motion.div
          className="absolute flex items-center justify-center"
          style={{ top: "50%", left: "50%", transform: "translate(-50%, -50%)" }}
        >
          {["a", "m", "a", "d", "h", "a", "n"].map((letter, index) => (
            <motion.span
              key={index}
              custom={index}
              initial={{ opacity: 0, x: -20 }}
              animate={letterControls}
              className="text-[60px] font-bold text-[#6D28D9]"
              style={{ marginLeft: "10px" }}
            >
              {letter}
            </motion.span>
          ))}
        </motion.div>
      </div>
    </div>
  );
};