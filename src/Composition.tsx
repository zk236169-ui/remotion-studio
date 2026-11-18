import React from 'react';
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
} from 'remotion';
import episodeData from '../public/current_episode.json';

interface Beat {
  isShopEnd: boolean;
  animType: string;
  clip: string;
  audio: string;
  frames: number;
  tag: string;
  headline: string;
  subline: string;
  accent: string;
}

// Custom 60fps Animated Motion Graphics for Top 30% Deck
const TopSceneAnimation: React.FC<{ animType: string; accent: string; frame: number; fps: number; frames: number }> = ({
  animType,
  accent,
  frame,
  fps,
  frames,
}) => {
  const prog = interpolate(frame, [0, Math.max(1, frames - 15)], [0, 1], { extrapolateRight: 'clamp' });
  const pop = spring({ frame, fps, config: { damping: 12, stiffness: 130 } });
  const pulse = Math.sin(frame * 0.14) * 0.06 + 1;

  switch (animType) {
    case 'peeling_wall': {
      const peelAngle = interpolate(prog, [0.15, 0.85], [0, 58], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      const crackLen = interpolate(prog, [0, 0.6], [0, 120], { extrapolateRight: 'clamp' });
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          {/* Concrete Wall Base */}
          <rect x="40" y="25" width="380" height="140" rx="16" fill="#1E293B" stroke="#475569" strokeWidth="3" />
          {/* Cracks appearing */}
          <path d={`M140,35 L165,85 L145,130 L170,160`} stroke="#EF4444" strokeWidth="4" fill="none" strokeDasharray="160" strokeDashoffset={160 - crackLen * 1.3} />
          <path d={`M290,30 L270,80 L300,125`} stroke="#EF4444" strokeWidth="3.5" fill="none" strokeDasharray="140" strokeDashoffset={140 - crackLen * 1.1} />
          {/* Peeling Paint Flap */}
          <g transform={`translate(210, 40) rotate(${peelAngle})`}>
            <rect x="0" y="0" width="130" height="95" rx="10" fill="#F8FAFC" opacity="0.92" />
            <text x="65" y="54" textAnchor="middle" fill="#EF4444" fontSize="22" fontWeight="900">تقشير!</text>
          </g>
          {/* Warning Badge */}
          <circle cx="95" cy="95" r={30 * pulse} fill="#EF4444" opacity="0.22" />
          <circle cx="95" cy="95" r="20" fill="#EF4444" />
          <text x="95" y="103" textAnchor="middle" fill="#FFF" fontSize="26" fontWeight="900">!</text>
        </svg>
      );
    }

    case 'sun_heat': {
      const tempHeight = interpolate(prog, [0, 0.8], [20, 115], { extrapolateRight: 'clamp' });
      const rayRot = frame * 1.5;
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          {/* Blazing Sun */}
          <g transform={`translate(105, 95) rotate(${rayRot})`}>
            {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => (
              <line key={deg} x1="0" y1="-58" x2="0" y2="-42" stroke="#F59E0B" strokeWidth="5" strokeLinecap="round" transform={`rotate(${deg})`} />
            ))}
          </g>
          <circle cx="105" cy="95" r={32 * pulse} fill="#F59E0B" />
          {/* Heat Waves */}
          {[0, 1, 2].map((w) => (
            <path
              key={w}
              d={`M ${165 + w * 28} 55 Q ${180 + w * 28} 75 ${165 + w * 28} 95 T ${165 + w * 28} 135`}
              stroke="#FB923C"
              strokeWidth="4"
              fill="none"
              opacity={0.4 + Math.sin(frame * 0.2 + w) * 0.4}
            />
          ))}
          {/* Thermometer */}
          <rect x="295" y="25" width="32" height="135" rx="16" fill="#0F172A" stroke="#94A3B8" strokeWidth="3" />
          <rect x="303" y={150 - tempHeight} width="16" height={tempHeight} rx="8" fill="#EF4444" />
          <text x="385" y="105" textAnchor="middle" fill="#FBBF24" fontSize="34" fontWeight="900">50°C</text>
        </svg>
      );
    }

    case 'primer_bond': {
      const teethShift = interpolate(prog, [0.1, 0.7], [45, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          {/* Concrete Layer */}
          <rect x="45" y="115" width="370" height="50" rx="10" fill="#334155" />
          <text x="230" y="147" textAnchor="middle" fill="#CBD5E1" fontSize="20" fontWeight="800">الجدار الخرساني</text>
          {/* Interlocking Primer Anchor Layer */}
          <g transform={`translate(0, ${-teethShift})`}>
            <rect x="45" y="72" width="370" height="43" rx="8" fill="#10B981" />
            {[80, 140, 200, 260, 320, 380].map((x) => (
              <polygon key={x} points={`${x-12},115 ${x+12},115 ${x},130`} fill="#10B981" />
            ))}
            <text x="230" y="100" textAnchor="middle" fill="#022C22" fontSize="21" fontWeight="900">طبقة برايمر عازل ورابط</text>
          </g>
          {/* Topcoat */}
          <rect x="45" y="25" width="370" height="40" rx="10" fill="#38BDF8" opacity={interpolate(prog, [0.5, 0.9], [0, 1], { extrapolateLeft: 'clamp' })} />
          <text x="230" y="52" textAnchor="middle" fill="#082F49" fontSize="20" fontWeight="900" opacity={interpolate(prog, [0.5, 0.9], [0, 1], { extrapolateLeft: 'clamp' })}>
            الدهان النهائي ثابت 100%
          </text>
        </svg>
      );
    }

    case 'roller_stroke': {
      const rollerX = interpolate(prog, [0, 0.85], [60, 360], { extrapolateRight: 'clamp' });
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          <rect x="45" y="35" width="370" height="120" rx="16" fill="#1E293B" stroke="#334155" strokeWidth="3" />
          {/* Painted Swath */}
          <rect x="45" y="35" width={Math.max(10, rollerX - 45)} height="120" rx="16" fill={accent} opacity="0.88" />
          {/* Moving Roller */}
          <g transform={`translate(${rollerX}, 45)`}>
            <rect x="-14" y="0" width="28" height="95" rx="8" fill="#FFFFFF" stroke="#0F172A" strokeWidth="3" />
            <path d="M 0 95 L 0 115 L -18 128 L -18 142" stroke="#94A3B8" strokeWidth="5" fill="none" strokeLinecap="round" />
          </g>
          <text x="230" y="104" textAnchor="middle" fill="#FFFFFF" fontSize="30" fontWeight="900">
            تغطية {Math.round(prog * 100)}%
          </text>
        </svg>
      );
    }

    case 'color_mixer': {
      const dropY = (frame * 6) % 75;
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          {/* Pigment Nozzles */}
          {['#EF4444', '#F59E0B', '#38BDF8'].map((col, idx) => (
            <g key={col} transform={`translate(${145 + idx * 85}, 20)`}>
              <rect x="-10" y="0" width="20" height="24" rx="4" fill="#64748B" />
              <circle cx="0" cy={28 + ((dropY + idx * 25) % 65)} r="8" fill={col} />
            </g>
          ))}
          {/* Swirling Paint Bucket */}
          <rect x="120" y="95" width="220" height="80" rx="16" fill="#1E293B" stroke="#94A3B8" strokeWidth="3" />
          <ellipse cx="230" cy="105" rx="95" ry="18" fill={accent} transform={`scale(${pulse} 1)`} style={{ transformOrigin: '230px 105px' }} />
          <text x="230" y="150" textAnchor="middle" fill="#F8FAFC" fontSize="22" fontWeight="900">خلط كمبيوتر دقيق 100%</text>
        </svg>
      );
    }

    case 'cost_comparison': {
      const cheapBar = interpolate(prog, [0, 0.7], [0, 145], { extrapolateRight: 'clamp' });
      const proBar = interpolate(prog, [0, 0.7], [0, 75], { extrapolateRight: 'clamp' });
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          {/* Cheap Paint Bar */}
          <rect x="70" y={155 - cheapBar} width="120" height={cheapBar} rx="12" fill="#EF4444" />
          <text x="130" y="178" textAnchor="middle" fill="#FCA5A5" fontSize="19" fontWeight="800">رخيص (تعيده مرتين)</text>
          <text x="130" y={145 - cheapBar} textAnchor="middle" fill="#FFF" fontSize="22" fontWeight="900">2X خسارة</text>
          {/* Original Paint Bar */}
          <rect x="270" y={155 - proBar} width="120" height={proBar} rx="12" fill="#10B981" />
          <text x="330" y="178" textAnchor="middle" fill="#6EE7B7" fontSize="19" fontWeight="800">أصلي (يدوم سنين)</text>
          <text x="330" y={145 - proBar} textAnchor="middle" fill="#FFF" fontSize="22" fontWeight="900">توفير 50%</text>
        </svg>
      );
    }

    case 'washable_shield': {
      const wipeX = interpolate(prog, [0.2, 0.85], [85, 345], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
      return (
        <svg width="460" height="190" viewBox="0 0 460 190">
          <rect x="55" y="28" width="350" height="134" rx="18" fill="#F1F5F9" />
          {/* Stain disappearing as wipe passes */}
          {wipeX < 230 && (
            <circle cx="220" cy="95" r="34" fill="#78350F" opacity={interpolate(wipeX, [160, 230], [0.85, 0], { extrapolateLeft: 'clamp' })} />
          )}
          {/* Clean Sparkles after wipe */}
          {wipeX > 220 && (
            <text x="200" y="105" textAnchor="middle" fill="#0284C7" fontSize="28" fontWeight="900">✨ نظيف 100% ✨</text>
          )}
          {/* Moving Sponge */}
          <rect x={wipeX - 28} y="55" width="56" height="80" rx="14" fill="#38BDF8" stroke="#0369A1" strokeWidth="3" />
        </svg>
      );
    }

    default: {
      // Animated Brands / Calculator / Shield Emblem
      return (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 22,
            height: 185,
            transform: `scale(${pop})`,
          }}
        >
          {['JOTUN', '777', 'NATIONAL'].map((b, i) => (
            <div
              key={b}
              style={{
                backgroundColor: i === 1 ? accent : 'rgba(255,255,255,0.08)',
                color: i === 1 ? '#090D16' : '#FFFFFF',
                border: `2px solid ${accent}`,
                borderRadius: 20,
                padding: '22px 28px',
                fontSize: 30,
                fontWeight: 900,
                transform: `translateY(${Math.sin(frame * 0.12 + i * 1.4) * 8}px)`,
                boxShadow: `0 12px 28px ${accent}33`,
              }}
            >
              {b}
            </div>
          ))}
        </div>
      );
    }
  }
};

const BeatScene: React.FC<{
  beat: Beat;
  index: number;
  totalBeats: number;
  shopName: string;
  locationText: string;
  whatsapp: string;
}> = ({ beat, index, totalBeats, shopName, locationText, whatsapp }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 130, mass: 0.8 },
  });

  // Dynamic camera punch-in + subtle rhythmic movement on bottom 70% stock video so it never feels static
  const baseZoom = interpolate(frame, [0, beat.frames], [1.02, 1.15], { extrapolateRight: 'clamp' });
  const beatBounce = Math.sin(frame * 0.16) * 0.012;
  const panX = Math.sin(frame * 0.04) * 14;

  const progressPct = ((index + Math.min(1, frame / beat.frames)) / totalBeats) * 100;

  if (beat.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#090D16',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
        }}
      >
        <Audio src={staticFile(beat.audio)} />
        <div style={{ position: 'relative', width: '100%', height: '54%', overflow: 'hidden' }}>
          <Img
            src={staticFile('assets/shop_front.jpg')}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${baseZoom})`,
            }}
          />
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(180deg, rgba(9,13,22,0.15) 0%, #090D16 100%)',
            }}
          />
        </div>

        <div
          style={{
            flex: 1,
            padding: '20px 52px 60px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            transform: `translateY(${interpolate(enterSpring, [0, 1], [35, 0])}px)`,
            opacity: enterSpring,
          }}
        >
          <div
            style={{
              backgroundColor: beat.accent,
              color: '#052E16',
              fontWeight: 900,
              fontSize: 30,
              padding: '10px 32px',
              borderRadius: 999,
              marginBottom: 18,
            }}
          >
            {beat.tag}
          </div>

          <div style={{ color: '#FFFFFF', fontSize: 62, fontWeight: 900, marginBottom: 14 }}>
            {shopName}
          </div>

          <div style={{ color: '#CBD5E1', fontSize: 28, fontWeight: 600, marginBottom: 30, lineHeight: 1.4 }}>
            {locationText}
          </div>

          <div
            style={{
              background: 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)',
              border: '2px solid #4ADE80',
              borderRadius: 24,
              padding: '20px 46px',
              color: '#FFFFFF',
              fontSize: 42,
              fontWeight: 900,
              letterSpacing: 2,
            }}
          >
            WhatsApp: {whatsapp}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090D16',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
      }}
    >
      <Audio src={staticFile(beat.audio)} />

      {/* TOP 30% ANIMATED EXPLAINER DECK (576px) */}
      <div
        style={{
          height: 576,
          width: '100%',
          background: `radial-gradient(circle at 50% 25%, ${beat.accent}26 0%, #0B1120 80%)`,
          borderBottom: `4px solid ${beat.accent}`,
          padding: '42px 44px 26px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          boxSizing: 'border-box',
          zIndex: 10,
        }}
      >
        {/* Top Bar: Shop Brand + Tag Pill + Counter */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div
            style={{
              backgroundColor: beat.accent,
              color: '#090D16',
              fontSize: 24,
              fontWeight: 900,
              padding: '6px 22px',
              borderRadius: 999,
            }}
          >
            {beat.tag}
          </div>

          <div style={{ color: '#E2E8F0', fontSize: 24, fontWeight: 800 }}>
            {shopName}
          </div>

          <div
            style={{
              color: '#94A3B8',
              fontSize: 22,
              fontWeight: 700,
              backgroundColor: 'rgba(15,23,42,0.85)',
              padding: '6px 16px',
              borderRadius: 10,
            }}
          >
            {index + 1} / {totalBeats - 1}
          </div>
        </div>

        {/* Center: Live Animated Diagram / Visual Metaphor */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '4px 0' }}>
          <TopSceneAnimation
            animType={beat.animType}
            accent={beat.accent}
            frame={frame}
            fps={fps}
            frames={beat.frames}
          />
        </div>

        {/* Bottom of Top Deck: Kinetic Headline & Emotional Caption */}
        <div style={{ textAlign: 'center' }}>
          <div
            style={{
              color: '#FFFFFF',
              fontSize: 44,
              fontWeight: 900,
              lineHeight: 1.2,
              marginBottom: 8,
              transform: `translateY(${interpolate(enterSpring, [0, 1], [18, 0])}px)`,
              opacity: enterSpring,
            }}
          >
            {beat.headline}
          </div>
          <div style={{ color: '#CBD5E1', fontSize: 26, fontWeight: 600, marginBottom: 12 }}>
            {beat.subline}
          </div>
          <div
            style={{
              width: '100%',
              height: 7,
              backgroundColor: 'rgba(255,255,255,0.1)',
              borderRadius: 999,
              overflow: 'hidden',
            }}
          >
            <div style={{ width: `${progressPct}%`, height: '100%', backgroundColor: beat.accent }} />
          </div>
        </div>
      </div>

      {/* BOTTOM 70% DYNAMICALLY EDITED FOOTAGE (1344px) */}
      <div
        style={{
          height: 1344,
          width: '100%',
          position: 'relative',
          overflow: 'hidden',
          backgroundColor: '#020617',
        }}
      >
        {beat.clip ? (
          <OffthreadVideo
            src={staticFile(beat.clip)}
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${baseZoom + beatBounce}) translateX(${panX}px)`,
            }}
          />
        ) : null}

        {/* Subtle Flash Transition on Scene Entry */}
        {frame < 8 && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              backgroundColor: '#FFFFFF',
              opacity: interpolate(frame, [0, 8], [0.28, 0]),
              pointerEvents: 'none',
            }}
          />
        )}

        {/* Cinematic Vignette */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(180deg, rgba(9,13,22,0.3) 0%, rgba(9,13,22,0) 20%, rgba(9,13,22,0) 80%, rgba(9,13,22,0.6) 100%)',
            pointerEvents: 'none',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const KhyberAnimatedDeckAR: React.FC = () => {
  const beats = episodeData.beats as Beat[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#090D16' }}>
      {beats.map((beat, idx) => {
        const from = offset;
        offset += beat.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={beat.frames}>
            <BeatScene
              beat={beat}
              index={idx}
              totalBeats={beats.length}
              shopName={episodeData.shopName}
              locationText={episodeData.locationText}
              whatsapp={episodeData.whatsapp}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};