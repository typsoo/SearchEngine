"use client";

import { useEffect, useRef } from "react";

export default function MorphingBackground() {
  const interactiveRef = useRef<HTMLDivElement>(null);

  const current = useRef({ x: 0, y: 0 });
  const target = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      target.current = { x: e.clientX, y: e.clientY };
    };

    window.addEventListener("mousemove", handleMouseMove);

    let animationFrameId: number;

    const animate = () => {
      current.current.x += (target.current.x - current.current.x) / 20;
      current.current.y += (target.current.y - current.current.y) / 20;

      if (interactiveRef.current) {
        interactiveRef.current.style.transform = `translate(${Math.round(current.current.x)}px, ${Math.round(current.current.y)}px)`;
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden bg-slate-50">
      <svg className="hidden">
        <defs>
          <filter id="goo">
            <feGaussianBlur
              in="SourceGraphic"
              stdDeviation="10"
              result="blur"
            />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
              result="goo"
            />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>

      <div className="gradients-container absolute inset-0 h-full w-full opacity-70">
        <div className="g1 absolute rounded-full mix-blend-multiply" />
        <div className="g2 absolute rounded-full mix-blend-multiply" />
        <div className="g3 absolute rounded-full mix-blend-multiply" />
        <div className="g4 absolute rounded-full mix-blend-multiply" />

        <div
          ref={interactiveRef}
          className="interactive absolute rounded-full mix-blend-multiply"
        />
      </div>

      <style jsx>{`
        .gradients-container {
          /* Soft pastel colors for a light theme UI */
          --color1: 173, 216, 230; /* Light Blue */
          --color2: 255, 182, 193; /* Light Pink */
          --color3: 221, 160, 221; /* Plum / Soft Purple */
          --color4: 240, 230, 140; /* Soft Yellow */
          --color-interactive: 135, 206, 250; /* Sky Blue */

          /* Dynamic size based on viewport */
          --circle-size: 80vw;

          /* Apply the SVG goo filter and add an extra blur for smoothness */
          filter: url(#goo) blur(40px);
        }

        @media (min-width: 768px) {
          .gradients-container {
            --circle-size: 50vw;
          }
        }

        .g1,
        .g2,
        .g3,
        .g4,
        .interactive {
          width: var(--circle-size);
          height: var(--circle-size);
        }

        .g1 {
          background: radial-gradient(
              circle at center,
              rgba(var(--color1), 0.8) 0,
              rgba(var(--color1), 0) 50%
            )
            no-repeat;
          top: calc(50% - var(--circle-size) / 2);
          left: calc(50% - var(--circle-size) / 2);
          transform-origin: center center;
          animation: moveVertical 30s ease-in-out infinite;
        }

        .g2 {
          background: radial-gradient(
              circle at center,
              rgba(var(--color2), 0.8) 0,
              rgba(var(--color2), 0) 50%
            )
            no-repeat;
          top: calc(50% - var(--circle-size) / 2);
          left: calc(50% - var(--circle-size) / 2);
          /* Offset the origin to create a sweeping circular motion */
          transform-origin: calc(50% - 400px);
          animation: moveInCircle 20s reverse infinite;
        }

        .g3 {
          background: radial-gradient(
              circle at center,
              rgba(var(--color3), 0.8) 0,
              rgba(var(--color3), 0) 50%
            )
            no-repeat;
          top: calc(50% - var(--circle-size) / 2 + 200px);
          left: calc(50% - var(--circle-size) / 2 - 500px);
          transform-origin: calc(50% + 400px);
          animation: moveInCircle 40s linear infinite;
        }

        .g4 {
          background: radial-gradient(
              circle at center,
              rgba(var(--color4), 0.8) 0,
              rgba(var(--color4), 0) 50%
            )
            no-repeat;
          top: calc(50% - var(--circle-size) / 2);
          left: calc(50% - var(--circle-size) / 2);
          transform-origin: calc(50% - 200px);
          animation: moveHorizontal 40s ease-in-out infinite;
        }

        .interactive {
          background: radial-gradient(
              circle at center,
              rgba(var(--color-interactive), 0.8) 0,
              rgba(var(--color-interactive), 0) 50%
            )
            no-repeat;
          /* Offset by half the size so the cursor is exactly in the center */
          top: calc(var(--circle-size) / -2);
          left: calc(var(--circle-size) / -2);
          opacity: 0.9;
        }

        @keyframes moveInCircle {
          0% {
            transform: rotate(0deg);
          }
          50% {
            transform: rotate(180deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }

        @keyframes moveVertical {
          0% {
            transform: translateY(-50%);
          }
          50% {
            transform: translateY(50%);
          }
          100% {
            transform: translateY(-50%);
          }
        }

        @keyframes moveHorizontal {
          0% {
            transform: translateX(-50%) translateY(-10%);
          }
          50% {
            transform: translateX(50%) translateY(10%);
          }
          100% {
            transform: translateX(-50%) translateY(-10%);
          }
        }
      `}</style>
    </div>
  );
}
