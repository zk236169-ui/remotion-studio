import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type VisualType =
  | "peel_wall"
  | "no_primer"
  | "cheap_redo"
  | "primer_grip"
  | "roller_coat"
  | "pc_mix"
  | "room_glow"
  | "tape_peel"
  | "wash_stain"
  | "sun_shield"
  | "free_calc"
  | "brands_trio"
  | "shop_pin";

export interface AnimatedBeat {
  isShopEnd: boolean;
  visualType: VisualType;
  clip?: string;
  audio: string;
  frames: number;
  tag: string;
  headline: string;
  accent: string;
}

export interface AnimatedDeckProps {
  shopName: string;
  locationText: string;
  whatsapp: string;
  totalFrames: number;
  beats: AnimatedBeat[];
}

/* ===================================================================== */
/* CUSTOM ANIMATED VISUAL ILLUSTRATIONS FOR THE TOP 30% STAGE (430x380)   */
/* ===================================================================== */
const TopVisualMotion: React.FC<{
  type: VisualType;
  accent: string;
  frame: number;
  fps: number;
  totalFrames: number;
}> = ({ type, accent, frame, fps, totalFrames }) => {
  const prog = interpolate(frame, [0, totalFrames], [0, 1], { extrapolateRight: "clamp" });
  const pop = spring({ frame, fps, config: { damping: 11, stiffness: 180, mass: 0.7 } });

  return (
    <div
      style={{
        width: 430,
        height: 375,
        borderRadius: 28,
        backgroundColor: "rgba(15, 25, 52, 0.92)",
        border: `3px solid ${accent}88`,
        boxShadow: `0 14px 36px rgba(0,0,0,0.45), inset 0 0 32px ${accent}22`,
        position: "relative",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
      }}
    >
      {/* 1. PEELING WALL ANIMATION */}
      {type === "peel_wall" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Concrete wall base */}
          <rect x="35" y="35" width="320" height="260" rx="18" fill="#334155" stroke="#64748B" strokeWidth="4" />
          {/* Rising moisture bubbles */}
          {[0, 1, 2, 3].map((i) => {
            const by = 260 - ((frame * 2.4 + i * 55) % 210);
            const r = 10 + Math.sin(frame * 0.2 + i) * 4;
            return <circle key={i} cx={95 + i * 65} cy={by} r={r} fill="#38BDF8" opacity="0.75" />;
          })}
          {/* Curling / peeling paint sheet */}
          <path
            d={`M 35 35 L 355 35 L 355 ${295 - prog * 175} Q ${210} ${250 - prog * 195} 35 ${295 - prog * 130} Z`}
            fill="#F8FAFC"
            stroke="#EF4444"
            strokeWidth="4"
          />
          {/* Curled flap underside */}
          <path
            d={`M 35 ${295 - prog * 130} Q 195 ${250 - prog * 195} 355 ${295 - prog * 175} Q 200 ${310 - prog * 140} 35 ${295 - prog * 130} Z`}
            fill="#EF4444"
          />
        </svg>
      )}

      {/* 2. NO PRIMER / REJECTED PAINT DROP */}
      {type === "no_primer" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Unprimed dusty wall */}
          <rect x="45" y="195" width="300" height="95" rx="16" fill="#475569" stroke="#94A3B8" strokeWidth="4" />
          {/* Bouncing paint drop */}
          <g transform={`translate(195, ${95 + Math.abs(Math.sin(frame * 0.14)) * 75})`}>
            <path d="M0 -34 C22 -4 28 14 28 24 A28 28 0 1 1 -28 24 C-28 14 -22 -4 0 -34 Z" fill="#F59E0B" />
          </g>
          {/* Flashing Red Warning Ring & X */}
          <g transform={`translate(195, 165) scale(${0.85 + Math.sin(frame * 0.25) * 0.08})`}>
            <circle cx="0" cy="0" r="68" fill="rgba(239,68,68,0.22)" stroke="#EF4444" strokeWidth="8" />
            <line x1="-28" y1="-28" x2="28" y2="28" stroke="#EF4444" strokeWidth="10" strokeLinecap="round" />
            <line x1="28" y1="-28" x2="-28" y2="28" stroke="#EF4444" strokeWidth="10" strokeLinecap="round" />
          </g>
        </svg>
      )}

      {/* 3. CHEAP PAINT FADING & 2X REDO LOOP */}
      {type === "cheap_redo" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Wall fading from bright to dull grey */}
          <rect
            x="55"
            y="45"
            width="280"
            height="240"
            rx="22"
            fill="#64748B"
            opacity={interpolate(prog, [0, 1], [1, 0.32])}
          />
          {/* Rotating 2X Redo Arrows */}
          <g transform={`translate(195, 165) rotate(${frame * 2.2})`}>
            <circle cx="0" cy="0" r="82" fill="none" stroke="#EF4444" strokeWidth="10" strokeDasharray="180 70" strokeLinecap="round" />
          </g>
          <text x="195" y="182" textAnchor="middle" fill="#FFFFFF" fontSize="56" fontWeight="900">
            2X
          </text>
        </svg>
      )}

      {/* 4. PRIMER GRIPPING WALL PORES */}
      {type === "primer_grip" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Wall substrate */}
          <rect x="40" y="180" width="310" height="110" rx="16" fill="#334155" />
          {/* Primer layer dropping & locking in */}
          <g transform={`translate(0, ${interpolate(pop, [0, 1], [-90, 0])})`}>
            <rect x="40" y="115" width="310" height="72" rx="12" fill="#10B981" />
            {[75, 135, 195, 255, 315].map((gx, idx) => (
              <polygon
                key={idx}
                points={`${gx - 14},185 ${gx + 14},185 ${gx},${185 + prog * 38}`}
                fill="#10B981"
              />
            ))}
          </g>
          {/* Checkmark badge */}
          <circle cx="195" cy="72" r="34" fill="#10B981" />
          <polyline points="178,72 191,85 214,60" fill="none" stroke="#070B14" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}

      {/* 5. ANIMATED PAINT ROLLER COATING */}
      {type === "roller_coat" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          <rect x="35" y="35" width="320" height="260" rx="18" fill="#1E293B" />
          {/* Painted thick swath following roller */}
          <rect
            x="35"
            y="75"
            width={interpolate(prog, [0, 1], [40, 290])}
            height="135"
            rx="12"
            fill="#38BDF8"
          />
          {/* Moving Roller */}
          <g transform={`translate(${interpolate(prog, [0, 1], [65, 305])}, 75)`}>
            <rect x="-18" y="0" width="36" height="135" rx="10" fill="#F8FAFC" stroke="#0284C7" strokeWidth="4" />
            <path d="M 18 68 L 42 68 L 42 155 L 0 155 L 0 185" fill="none" stroke="#94A3B8" strokeWidth="7" strokeLinecap="round" />
            <rect x="-12" y="180" width="24" height="58" rx="8" fill="#F59E0B" />
          </g>
        </svg>
      )}

      {/* 6. COMPUTER COLOR MIXING SWIRL */}
      {type === "pc_mix" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Falling pigment drops */}
          {["#EC4899", "#38BDF8", "#F59E0B"].map((col, idx) => {
            const dy = ((frame * 4.5 + idx * 35) % 110);
            return <circle key={idx} cx={145 + idx * 50} cy={32 + dy} r="12" fill={col} />;
          })}
          {/* Paint Can Rim & Rotating Color Vortex */}
          <circle cx="195" cy="205" r="96" fill="#0F172A" stroke="#CBD5E1" strokeWidth="8" />
          <g transform={`translate(195, 205) rotate(${frame * 4.2})`}>
            <path d="M0 0 L0 -80 A80 80 0 0 1 76 -25 Z" fill="#F59E0B" />
            <path d="M0 0 L76 -25 A80 80 0 0 1 47 65 Z" fill="#EC4899" />
            <path d="M0 0 L47 65 A80 80 0 0 1 -65 47 Z" fill="#38BDF8" />
            <path d="M0 0 L-65 47 A80 80 0 0 1 0 -80 Z" fill="#10B981" />
          </g>
          <circle cx="195" cy="205" r="26" fill="#FEF3C7" />
        </svg>
      )}

      {/* 7. LUXURY ROOM LIGHTING UP */}
      {type === "room_glow" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Room wall & arch */}
          <rect x="45" y="40" width="300" height="250" rx="22" fill="#F5EFE6" />
          <path d="M 115 290 L 115 140 A 80 80 0 0 1 275 140 L 275 290 Z" fill="#E6D5B8" />
          {/* Warm glowing sunlight rays */}
          <circle cx="195" cy="125" r={45 + Math.sin(frame * 0.15) * 10} fill="#F59E0B" opacity="0.45" />
          {/* Minimalist sofa silhouette */}
          <rect x="95" y="220" width="200" height="52" rx="16" fill="#78350F" />
          <rect x="85" y="238" width="220" height="36" rx="12" fill="#92400E" />
        </svg>
      )}

      {/* 8. CRISP PAINTER'S TAPE PEEL */}
      {type === "tape_peel" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Two-tone crisp painted wall */}
          <rect x="45" y="40" width="150" height="250" rx="12" fill="#0EA5E9" />
          <rect x="195" y="40" width="150" height="250" rx="12" fill="#F8FAFC" />
          {/* Peeling yellow painter's tape strip */}
          <rect
            x="181"
            y={40 + prog * 195}
            width="28"
            height={250 - prog * 195}
            fill="#FACC15"
          />
          {/* Curled tape roll */}
          <circle cx="195" cy={48 + prog * 195} r="20" fill="#EAB308" stroke="#FEF08A" strokeWidth="4" />
        </svg>
      )}

      {/* 9. WASHABLE WALL WIPING STAIN */}
      {type === "wash_stain" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          <rect x="45" y="40" width="300" height="250" rx="22" fill="#F1F5F9" />
          {/* Coffee stain fading away as sponge passes */}
          <circle
            cx="195"
            cy="165"
            r="52"
            fill="#78350F"
            opacity={interpolate(prog, [0.15, 0.75], [0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
          />
          {/* Animated Wiping Sponge */}
          <g transform={`translate(${145 + Math.sin(frame * 0.25) * 65}, 135)`}>
            <rect x="0" y="0" width="95" height="62" rx="16" fill="#38BDF8" stroke="#0284C7" strokeWidth="4" />
            <circle cx="24" cy="22" r="5" fill="#E0F2FE" />
            <circle cx="66" cy="36" r="6" fill="#E0F2FE" />
          </g>
          {/* Clean Sparkles */}
          {prog > 0.55 && (
            <g fill="#10B981">
              <circle cx="135" cy="110" r={8 + Math.sin(frame * 0.3) * 3} />
              <circle cx="265" cy="215" r={10 + Math.cos(frame * 0.3) * 3} />
            </g>
          )}
        </svg>
      )}

      {/* 10. 50C SUN SHIELD BOUNCING HEAT RAYS */}
      {type === "sun_shield" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Blazing Sun */}
          <circle cx="95" cy="95" r={42 + Math.sin(frame * 0.2) * 4} fill="#F59E0B" />
          {/* Coated Villa Wall */}
          <rect x="235" y="55" width="95" height="230" rx="14" fill="#F8FAFC" stroke="#10B981" strokeWidth="8" />
          {/* Bouncing Heat Arrows */}
          {[0, 1, 2].map((i) => {
            const shift = ((frame * 3 + i * 25) % 45);
            return (
              <g key={i} transform={`translate(${shift * 0.4}, ${i * 55})`}>
                <polyline
                  points="135,95 220,125 155,155"
                  fill="none"
                  stroke="#EF4444"
                  strokeWidth="6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </g>
            );
          })}
        </svg>
      )}

      {/* 11. FREE AREA CALCULATOR & EXACT BUCKET */}
      {type === "free_calc" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Wall Blueprint Grid */}
          <rect x="45" y="45" width="185" height="235" rx="14" fill="#1E293B" stroke="#38BDF8" strokeWidth="4" />
          {/* Scanning Laser Line */}
          <line
            x1="50"
            y1={55 + ((frame * 3.5) % 215)}
            x2="225"
            y2={55 + ((frame * 3.5) % 215)}
            stroke="#10B981"
            strokeWidth="5"
          />
          <text x="137" y="172" textAnchor="middle" fill="#38BDF8" fontSize="34" fontWeight="900">
            m²
          </text>
          {/* Exact Single Paint Bucket */}
          <g transform={`translate(295, 175) scale(${pop})`}>
            <rect x="-42" y="-45" width="84" height="96" rx="12" fill="#10B981" />
            <rect x="-48" y="-54" width="96" height="16" rx="6" fill="#F8FAFC" />
            <polyline points="-18,4 -4,18 22,-10" fill="none" stroke="#070B14" strokeWidth="8" strokeLinecap="round" />
          </g>
        </svg>
      )}

      {/* 12. REAL BRANDS PODIUM (JOTUN • 777 • NATIONAL) */}
      {type === "brands_trio" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {[
            { label: "JOTUN", ar: "جوتن", x: 75, col: "#EF4444", delay: 0 },
            { label: "777", ar: "777", x: 195, col: "#F59E0B", delay: 6 },
            { label: "NATIONAL", ar: "ناشونال", x: 315, col: "#38BDF8", delay: 12 },
          ].map((b, idx) => {
            const bPop = spring({ frame: Math.max(0, frame - b.delay), fps, config: { damping: 10, stiffness: 190 } });
            return (
              <g key={idx} transform={`translate(${b.x}, ${interpolate(bPop, [0, 1], [310, 175])})`}>
                <rect x="-46" y="-58" width="92" height="116" rx="14" fill={b.col} stroke="#FFFFFF" strokeWidth="3" />
                <rect x="-52" y="-68" width="104" height="16" rx="6" fill="#F8FAFC" />
                <text x="0" y="-4" textAnchor="middle" fill="#070B14" fontSize="22" fontWeight="900">
                  {b.ar}
                </text>
                <text x="0" y="24" textAnchor="middle" fill="#070B14" fontSize="14" fontWeight="900">
                  {b.label}
                </text>
              </g>
            );
          })}
        </svg>
      )}

      {/* 13. SHOP LOCATION PIN & WHATSAPP PULSE */}
      {type === "shop_pin" && (
        <svg width="390" height="330" viewBox="0 0 390 330">
          {/* Radar pulse rings */}
          <circle
            cx="195"
            cy="215"
            r={30 + ((frame * 1.8) % 85)}
            fill="none"
            stroke="#22C55E"
            strokeWidth="5"
            opacity={1 - ((frame * 1.8) % 85) / 85}
          />
          {/* Bouncing Map Pin */}
          <g transform={`translate(195, ${135 - Math.abs(Math.sin(frame * 0.14)) * 26})`}>
            <path
              d="M0 -68 C38 -68 64 -40 64 -6 C64 36 0 88 0 88 C0 88 -64 36 -64 -6 C-64 -40 -38 -68 0 -68 Z"
              fill="#22C55E"
              stroke="#FFFFFF"
              strokeWidth="5"
            />
            <circle cx="0" cy="-10" r="24" fill="#070B14" />
          </g>
        </svg>
      )}
    </div>
  );
};

const AnimatedBeatScene: React.FC<{
  beat: AnimatedBeat;
  index: number;
  totalBeats: number;
  props: AnimatedDeckProps;
}> = ({ beat, index, totalBeats, props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textPop = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 185, mass: 0.7 },
  });

  // Gentle forward push (always >= 1.0 so bottom 70% never zooms out or cuts in half)
  const pushIn = interpolate(frame, [0, beat.frames], [1.0, 1.055], {
    extrapolateRight: "clamp",
  });

  const slideX = interpolate(textPop, [0, 1], [36, 0]);
  const progressPct =
    ((index + interpolate(frame, [0, beat.frames], [0, 1], { extrapolateRight: "clamp" })) /
      totalBeats) *
    100;

  return (
    <AbsoluteFill style={{ backgroundColor: "#070B14", fontFamily: "Tahoma, Arial, sans-serif" }}>
      <Audio src={staticFile(beat.audio)} />
      {(index === 0 || beat.isShopEnd) && (
        <Audio src={staticFile("sfx/impact.mp3")} volume={0.40} />
      )}
      {index > 0 && !beat.isShopEnd && index % 2 === 1 && (
        <Audio src={staticFile("sfx/whoosh.mp3")} volume={0.22} />
      )}

      {/* ========================================================= */}
      {/* TOP 30% ANIMATED MOTION GRAPHICS + SHORT HOOK (0 -> 576px) */}
      {/* ========================================================= */}
      <div
        dir="rtl"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 576,
          background: "linear-gradient(165deg, #091124 0%, #111F42 60%, #0A1329 100%)",
          borderBottom: `6px solid ${beat.accent}`,
          padding: "28px 36px 20px 36px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxSizing: "border-box",
          zIndex: 10,
        }}
      >
        {/* Top Shop Header Bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 12, height: 38, borderRadius: 6, backgroundColor: beat.accent }} />
            <div style={{ color: "#FFFFFF", fontSize: 31, fontWeight: 900 }}>
              {props.shopName}
            </div>
          </div>
          <div
            style={{
              backgroundColor: "rgba(255,255,255,0.10)",
              border: `2px solid ${beat.accent}`,
              color: beat.accent,
              fontSize: 19,
              fontWeight: 900,
              padding: "6px 14px",
              borderRadius: 12,
            }}
          >
            {"جوتن • 777 • ناشونال"}
          </div>
        </div>

        {/* Center Split inside Top 30%: Short Arabic Hook (Right) + Animated Visual (Left) */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: 24,
            flex: 1,
            marginTop: 10,
            marginBottom: 10,
          }}
        >
          {/* Right Side: Clean, Short Punchy Text (No clutter) */}
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              gap: 16,
              transform: `translateX(${slideX}px)`,
              opacity: textPop,
            }}
          >
            <div
              style={{
                alignSelf: "flex-start",
                backgroundColor: beat.accent,
                color: "#070B14",
                fontSize: 24,
                fontWeight: 900,
                padding: "8px 20px",
                borderRadius: 14,
              }}
            >
              {beat.tag}
            </div>
            <div
              style={{
                color: "#FFFFFF",
                fontSize: beat.headline.length > 26 ? 40 : 46,
                fontWeight: 900,
                lineHeight: 1.25,
              }}
            >
              {beat.headline}
            </div>
          </div>

          {/* Left Side: Frame-by-Frame Animated Visual Illustration */}
          <TopVisualMotion
            type={beat.visualType}
            accent={beat.accent}
            frame={frame}
            fps={fps}
            totalFrames={beat.frames}
          />
        </div>

        {/* Bottom Progress Bar */}
        <div
          style={{
            width: "100%",
            height: 8,
            backgroundColor: "rgba(255,255,255,0.14)",
            borderRadius: 6,
            overflow: "hidden",
          }}
        >
          <div style={{ width: `${progressPct}%`, height: "100%", backgroundColor: beat.accent }} />
        </div>
      </div>

      {/* ========================================================= */}
      {/* BOTTOM 70% UNOBSTRUCTED LIVE VISUALS (576px -> 1920px)    */}
      {/* ========================================================= */}
      <div
        style={{
          position: "absolute",
          top: 576,
          left: 0,
          width: 1080,
          height: 1344,
          overflow: "hidden",
          backgroundColor: "#04070F",
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: `scale(${pushIn})`,
            transformOrigin: "center center",
          }}
        >
          {beat.isShopEnd ? (
            <Img
              src={staticFile("assets/shop_front.jpg")}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          ) : (
            beat.clip && (
              <OffthreadVideo
                src={staticFile(beat.clip)}
                muted
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            )
          )}
        </div>

        {/* Bottom WhatsApp & Location Card ONLY on the Final Shop Photo */}
        {beat.isShopEnd && (
          <div
            dir="rtl"
            style={{
              position: "absolute",
              bottom: 42,
              left: 36,
              right: 36,
              backgroundColor: "rgba(7, 11, 20, 0.94)",
              border: "3px solid #22C55E",
              borderRadius: 24,
              padding: "20px 26px",
              display: "flex",
              flexDirection: "column",
              gap: 10,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ color: "#FFFFFF", fontSize: 28, fontWeight: 900 }}>
                {"راسلنا واتساب الآن:"}
              </span>
              <span
                dir="ltr"
                style={{
                  backgroundColor: "#22C55E",
                  color: "#052E16",
                  fontSize: 34,
                  fontWeight: 900,
                  padding: "8px 22px",
                  borderRadius: 14,
                }}
              >
                {props.whatsapp}
              </span>
            </div>
            <div style={{ color: "#E2E8F0", fontSize: 23, fontWeight: 700 }}>
              {props.locationText}
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

export const KhyberAnimatedDeckAR: React.FC<AnimatedDeckProps> = (props) => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#070B14" }}>
      {props.beats.map((b, i) => {
        const from = cursor;
        cursor += b.frames;
        return (
          <Sequence key={i} from={from} durationInFrames={b.frames}>
            <AnimatedBeatScene beat={b} index={i} totalBeats={props.beats.length} props={props} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
