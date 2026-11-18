import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import wbData from '../public/current_whiteboard.json';

interface PaintScene {
  isShopEnd?: boolean;
  audio: string;
  frames: number;
  stepTag: string;
  title: string;
  narration: string;
  illustration: string;
  leftLabel?: string;
  rightLabel?: string;
  callout?: string;
  accent: string;
}

const WhiteboardSketch: React.FC<{
  scene: PaintScene;
  sceneIndex: number;
  p: number;
  frame: number;
}> = ({ scene, sceneIndex, p, frame }) => {
  const {
    illustration,
    leftLabel = 'بدون برايمر ❌',
    rightLabel = 'مع برايمر ✅',
    callout = 'نتيجة مضمونة 100%',
  } = scene;

  const draw = (len: number, start = 0, end = 0.68) => {
    const localP = interpolate(p, [start, end], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return len * (1 - localP);
  };

  const reveal = (start = 0.3, end = 0.6) =>
    interpolate(p, [start, end], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });

  const pulse = Math.sin(frame * 0.18) * 0.07 + 1;
  const shake = p > 0.45 && p < 0.75 ? Math.sin(frame * 0.9) * 5 : 0;
  const penX = interpolate(p, [0, 0.82], [140, 820], { extrapolateRight: 'clamp' });
  const penY = 300 + Math.sin(frame * 0.32) * 75;
  const showPen = p < 0.82;
  const gridId = `paperGrid_${sceneIndex}`;

  const renderIllustration = () => {
    switch (illustration) {
      case 'peeling_wall':
        return (
          <g transform={`translate(${shake}, 0)`}>
            <rect x="120" y="90" width="720" height="430" rx="18" fill="#F8FAFC" stroke="#1E293B" strokeWidth="7" strokeDasharray="2400" strokeDashoffset={draw(2400, 0, 0.32)} />
            <path d="M 220 180 Q 320 160 360 250 Q 290 290 210 260 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="6" strokeDasharray="600" strokeDashoffset={draw(600, 0.12, 0.45)} />
            <path d="M 520 210 Q 650 190 700 310 Q 590 360 510 310 Z" fill="#FEE2E2" stroke="#DC2626" strokeWidth="6" strokeDasharray="700" strokeDashoffset={draw(700, 0.18, 0.52)} />
            <circle cx="430" cy="370" r={38 * pulse} fill="#FCA5A5" stroke="#DC2626" strokeWidth="5" opacity={reveal(0.22, 0.45)} />
            <circle cx="640" cy="410" r={28 * pulse} fill="#FCA5A5" stroke="#DC2626" strokeWidth="5" opacity={reveal(0.28, 0.5)} />
            <g opacity={reveal(0.4, 0.65)}>
              <circle cx="480" cy="305" r="95" fill="#DC2626" fillOpacity="0.14" stroke="#DC2626" strokeWidth="8" />
              <line x1="435" y1="260" x2="525" y2="350" stroke="#DC2626" strokeWidth="12" strokeLinecap="round" />
              <line x1="525" y1="260" x2="435" y2="350" stroke="#DC2626" strokeWidth="12" strokeLinecap="round" />
            </g>
            <g opacity={reveal(0.45, 0.7)}>
              <rect x="210" y="545" width="540" height="64" rx="14" fill="#DC2626" />
              <text x="480" y="588" textAnchor="middle" fill="#FFFFFF" fontSize="30" fontWeight="900">{callout}</text>
            </g>
          </g>
        );

      case 'moisture_pores':
        return (
          <g>
            <circle cx="740" cy="120" r={54 * pulse} fill="#FDE047" stroke="#D97706" strokeWidth="6" />
            <path d="M 620 150 Q 650 175 620 200" fill="none" stroke="#EA580C" strokeWidth="6" strokeLinecap="round" opacity={reveal(0.2, 0.45)} />
            <path d="M 665 170 Q 695 195 665 220" fill="none" stroke="#EA580C" strokeWidth="6" strokeLinecap="round" opacity={reveal(0.25, 0.5)} />
            <rect x="130" y="230" width="240" height="310" fill="#CBD5E1" stroke="#1E293B" strokeWidth="6" strokeDasharray="1200" strokeDashoffset={draw(1200, 0, 0.32)} />
            <text x="250" y="395" textAnchor="middle" fill="#1E293B" fontSize="28" fontWeight="900">خرسانة</text>
            <circle cx="330" cy="300" r="18" fill="#0284C7" opacity={reveal(0.2, 0.45)} />
            <circle cx="335" cy="385" r="22" fill="#0284C7" opacity={reveal(0.25, 0.5)} />
            <circle cx="328" cy="465" r="18" fill="#0284C7" opacity={reveal(0.3, 0.55)} />
            <path d="M 385 230 L 425 230 Q 495 340 435 540 L 385 540 Z" fill="#FDBA74" stroke="#DC2626" strokeWidth="6" strokeDasharray="900" strokeDashoffset={draw(900, 0.18, 0.55)} />
            <g opacity={reveal(0.4, 0.68)}>
              <line x1="355" y1="340" x2="530" y2="340" stroke="#DC2626" strokeWidth="8" strokeLinecap="round" />
              <polygon points="530,325 565,340 530,355" fill="#DC2626" />
              <rect x="575" y="295" width="275" height="90" rx="14" fill="#FEF2F2" stroke="#DC2626" strokeWidth="4" />
              <text x="712" y="348" textAnchor="middle" fill="#DC2626" fontSize="26" fontWeight="900">{callout}</text>
            </g>
          </g>
        );

      case 'wrong_vs_right':
        return (
          <g>
            <line x1="480" y1="80" x2="480" y2="570" stroke="#1E293B" strokeWidth="6" strokeDasharray="14 10" />
            <rect x="90" y="130" width="350" height="340" rx="18" fill="#FEF2F2" stroke="#DC2626" strokeWidth="6" strokeDasharray="1500" strokeDashoffset={draw(1500, 0, 0.35)} />
            <path d="M 150 220 L 230 300 L 180 390 M 320 200 L 270 310 L 360 380" fill="none" stroke="#DC2626" strokeWidth="6" strokeLinecap="round" opacity={reveal(0.22, 0.5)} />
            <rect x="115" y="495" width="300" height="58" rx="12" fill="#DC2626" opacity={reveal(0.3, 0.6)} />
            <text x="265" y="533" textAnchor="middle" fill="#FFFFFF" fontSize="26" fontWeight="900">{leftLabel}</text>

            <rect x="520" y="130" width="350" height="340" rx="18" fill="#ECFDF5" stroke="#16A34A" strokeWidth="6" strokeDasharray="1500" strokeDashoffset={draw(1500, 0.12, 0.5)} />
            <path d="M 620 300 L 675 355 L 785 235" fill="none" stroke="#16A34A" strokeWidth="14" strokeLinecap="round" strokeLinejoin="round" opacity={reveal(0.35, 0.65)} />
            <rect x="545" y="495" width="300" height="58" rx="12" fill="#16A34A" opacity={reveal(0.4, 0.7)} />
            <text x="695" y="533" textAnchor="middle" fill="#FFFFFF" fontSize="26" fontWeight="900">{rightLabel}</text>
          </g>
        );

      case 'funny_comparison':
        return (
          <g>
            <circle cx="290" cy="185" r="52" fill="#FEF3C7" stroke="#1E293B" strokeWidth="6" strokeDasharray="400" strokeDashoffset={draw(400, 0, 0.3)} />
            <circle cx="272" cy="175" r="6" fill="#1E293B" />
            <circle cx="308" cy="175" r="6" fill="#1E293B" />
            <ellipse cx="290" cy="205" rx="12" ry="16" fill="#DC2626" />
            <line x1="290" y1="237" x2="290" y2="410" stroke="#1E293B" strokeWidth="7" strokeLinecap="round" />
            <path d="M 290 280 L 210 340 M 290 280 L 370 340" stroke="#1E293B" strokeWidth="7" strokeLinecap="round" />
            <path d="M 290 410 L 240 520 M 290 410 L 340 520" stroke="#1E293B" strokeWidth="7" strokeLinecap="round" />
            <g opacity={reveal(0.3, 0.62)}>
              <rect x="420" y="150" width="440" height="230" rx="26" fill="#FEF9C3" stroke="#CA8A04" strokeWidth="6" />
              <polygon points="420,250 375,270 420,290" fill="#FEF9C3" stroke="#CA8A04" strokeWidth="5" />
              <text x="640" y="245" textAnchor="middle" fill="#1E293B" fontSize="32" fontWeight="900">دهان بدون أساس</text>
              <text x="640" y="305" textAnchor="middle" fill="#B45309" fontSize="30" fontWeight="900">مثل البدلة بدون قميص! 😂</text>
            </g>
          </g>
        );

      case 'roller_steps':
        return (
          <g>
            {[
              { y: 110, num: '1', text: 'صنفرة وتنظيف الجدار', color: '#0284C7', start: 0.05 },
              { y: 270, num: '2', text: 'وجه أساس (برايمر عازل)', color: '#D97706', start: 0.22 },
              { y: 430, num: '3', text: 'وجهين دهان أصلي مقاوم', color: '#16A34A', start: 0.40 },
            ].map((st, idx) => (
              <g key={idx} opacity={reveal(st.start, st.start + 0.22)}>
                <rect x="120" y={st.y} width="720" height="120" rx="20" fill="#FFFFFF" stroke={st.color} strokeWidth="6" />
                <circle cx="775" cy={st.y + 60} r="36" fill={st.color} />
                <text x="775" y={st.y + 72} textAnchor="middle" fill="#FFFFFF" fontSize="34" fontWeight="900">{st.num}</text>
                <text x="450" y={st.y + 72} textAnchor="middle" fill="#0F172A" fontSize="34" fontWeight="900">{st.text}</text>
              </g>
            ))}
          </g>
        );

      default:
        return (
          <g>
            {[
              { rot: -22, fill: '#38BDF8' },
              { rot: -8, fill: '#FBBF24' },
              { rot: 8, fill: '#34D399' },
              { rot: 22, fill: '#F87171' },
            ].map((sw, i) => (
              <g key={i} transform={`translate(480, 480) rotate(${sw.rot * reveal(0.1, 0.5)})`}>
                <rect x="-55" y="-330" width="110" height="310" rx="16" fill={sw.fill} stroke="#1E293B" strokeWidth="6" />
              </g>
            ))}
            <g opacity={reveal(0.35, 0.68)}>
              <rect x="200" y="510" width="560" height="72" rx="16" fill="#0F172A" />
              <text x="480" y="557" textAnchor="middle" fill="#FBBF24" fontSize="30" fontWeight="900">{callout}</text>
            </g>
          </g>
        );
    }
  };

  return (
    <div
      style={{
        width: 960,
        height: 640,
        backgroundColor: '#FFFFFF',
        border: '5px solid #1E293B',
        borderRadius: 28,
        boxShadow: '0 22px 50px rgba(15, 23, 42, 0.14)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <svg width="960" height="640" viewBox="0 0 960 640">
        <defs>
          <pattern id={gridId} width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2E8F0" strokeWidth="1.5" />
          </pattern>
        </defs>
        <rect width="960" height="640" fill={`url(#${gridId})`} />
        {renderIllustration()}
        {showPen && (
          <g transform={`translate(${penX}, ${penY}) rotate(-28)`}>
            <rect x="0" y="-14" width="150" height="28" rx="8" fill="#1E293B" />
            <rect x="115" y="-14" width="35" height="28" rx="4" fill="#DC2626" />
            <polygon points="0,-12 -28,0 0,12" fill="#FDE68A" stroke="#1E293B" strokeWidth="3" />
            <polygon points="-20,-4 -28,0 -20,4" fill="#DC2626" />
          </g>
        )}
      </svg>
    </div>
  );
};

const PaintWhiteboardSceneView: React.FC<{
  scene: PaintScene;
  index: number;
  total: number;
  shopName: string;
  locationText: string;
  whatsapp: string;
  offerText: string;
}> = ({ scene, index, total, shopName, locationText, whatsapp, offerText }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const p = interpolate(frame, [0, scene.frames], [0, 1], { extrapolateRight: 'clamp' });
  const pop = spring({ frame, fps, config: { damping: 13, stiffness: 150 } });
  const overallPct = ((index + p) / total) * 100;

  if (scene.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#FAF8F5',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '60px 45px',
          textAlign: 'center',
        }}
      >
        {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
        <div
          style={{
            transform: `scale(${pop})`,
            backgroundColor: '#FFFFFF',
            border: '6px solid #16A34A',
            borderRadius: 36,
            padding: '54px 42px',
            width: '100%',
            boxShadow: '0 28px 65px rgba(22, 163, 74, 0.22)',
          }}
        >
          <div
            style={{
              backgroundColor: '#DCFCE7',
              color: '#15803D',
              border: '3px solid #16A34A',
              fontSize: 32,
              fontWeight: 900,
              padding: '12px 34px',
              borderRadius: 999,
              display: 'inline-block',
              marginBottom: 26,
            }}
          >
            {offerText}
          </div>
          <div style={{ color: '#0F172A', fontSize: 68, fontWeight: 900, lineHeight: 1.2, marginBottom: 22 }}>
            {shopName}
          </div>
          <div style={{ color: '#475569', fontSize: 34, fontWeight: 700, lineHeight: 1.45, marginBottom: 38 }}>
            📍 {locationText}
          </div>
          <div
            style={{
              background: 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)',
              color: '#FFFFFF',
              fontSize: 46,
              fontWeight: 900,
              padding: '24px 48px',
              borderRadius: 24,
              display: 'inline-block',
              boxShadow: '0 16px 38px rgba(22, 163, 74, 0.38)',
              marginBottom: 28,
            }}
          >
            واتساب: {whatsapp}
          </div>
          <div style={{ color: '#1E293B', fontSize: 30, fontWeight: 800 }}>
            {scene.narration}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  const words = scene.narration.split(/\s+/).filter(Boolean);
  const activeWordIdx = Math.min(words.length - 1, Math.floor(p * words.length * 1.08));
  const chunkSize = 7;
  const chunkStart = Math.floor(activeWordIdx / chunkSize) * chunkSize;
  const visibleWords = words.slice(chunkStart, chunkStart + chunkSize);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#FAF8F5',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '75px 50px 95px 50px',
      }}
    >
      {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
      <div style={{ textAlign: 'center', width: '100%', transform: `scale(${pop})` }}>
        <div
          style={{
            backgroundColor: scene.accent,
            color: '#FFFFFF',
            fontSize: 28,
            fontWeight: 900,
            padding: '10px 30px',
            borderRadius: 999,
            display: 'inline-block',
            marginBottom: 18,
          }}
        >
          {scene.stepTag}
        </div>
        <div style={{ color: '#0F172A', fontSize: 54, fontWeight: 900, lineHeight: 1.25 }}>
          {scene.title}
        </div>
      </div>

      <WhiteboardSketch scene={scene} sceneIndex={index} p={p} frame={frame} />

      <div
        style={{
          width: '100%',
          backgroundColor: '#0F172A',
          borderBottom: `8px solid ${scene.accent}`,
          borderRadius: 24,
          padding: '28px 34px',
          textAlign: 'center',
          boxShadow: '0 20px 45px rgba(15, 23, 42, 0.25)',
        }}
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14 }}>
          {visibleWords.map((w, localIdx) => {
            const globalIdx = chunkStart + localIdx;
            const isCurrent = globalIdx === activeWordIdx;
            const isSpoken = globalIdx < activeWordIdx;
            return (
              <span
                key={globalIdx}
                style={{
                  fontSize: 42,
                  fontWeight: 900,
                  lineHeight: 1.3,
                  color: isCurrent ? '#FBBF24' : isSpoken ? '#FFFFFF' : 'rgba(255,255,255,0.48)',
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
      </div>

      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 10, backgroundColor: '#E2E8F0' }}>
        <div style={{ width: `${overallPct}%`, height: '100%', backgroundColor: scene.accent }} />
      </div>
    </AbsoluteFill>
  );
};

export const PaintWhiteboard9x16: React.FC = () => {
  const scenes = wbData.scenes as PaintScene[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#FAF8F5' }}>
      {scenes.map((sc, idx) => {
        const from = offset;
        offset += sc.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={sc.frames}>
            <PaintWhiteboardSceneView
              scene={sc}
              index={idx}
              total={scenes.length}
              shopName={wbData.shopName}
              locationText={wbData.locationText}
              whatsapp={wbData.whatsapp}
              offerText={wbData.offerText}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};