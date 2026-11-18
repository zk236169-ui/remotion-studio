import React from 'react';
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import wbData from '../public/current_whiteboard.json';

interface ProScene {
  isShopEnd?: boolean;
  audio: string;
  video?: string;
  visualType?: string;
  frames: number;
  stepTag: string;
  title: string;
  narration: string;
  statBadge?: string;
  leftMetric?: string;
  rightMetric?: string;
  accent: string;
  secondary?: string;
}

const ArchitecturalVisualCard: React.FC<{
  scene: ProScene;
  p: number;
  frame: number;
}> = ({ scene, p, frame }) => {
  const wipePct = interpolate(p, [0.1, 0.85], [18, 86], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const barGrow = interpolate(p, [0.1, 0.75], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const shimmer = Math.sin(frame * 0.14) * 14;

  switch (scene.visualType) {
    case 'sheen_comparison':
      return (
        <div
          style={{
            width: 960,
            height: 520,
            borderRadius: 28,
            backgroundColor: 'rgba(15, 23, 42, 0.88)',
            border: `3px solid ${scene.accent}`,
            padding: '28px 26px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
          }}
        >
          <div style={{ color: '#FBBF24', fontSize: 28, fontWeight: 900, textAlign: 'center' }}>
            مقارنة انعكاس الإضاءة وقابلية الغسيل
          </div>
          <div style={{ display: 'flex', gap: 18, height: 340 }}>
            {[
              { name: 'مطفي (Matte)', sub: 'يخفي عيوب اللياسة', shine: 0.08, wash: '40%', bg: '#334155' },
              { name: 'ربع لمعة (Eggshell)', sub: 'الأكثر طلباً للمجالس', shine: 0.35, wash: '85%', bg: '#B45309' },
              { name: 'نصف لمعة (Semi)', sub: 'مقاوم للغسيل اليومي', shine: 0.68, wash: '100%', bg: '#0369A1' },
            ].map((item, idx) => (
              <div
                key={idx}
                style={{
                  flex: 1,
                  borderRadius: 22,
                  background: `linear-gradient(${135 + shimmer}deg, ${item.bg} 0%, rgba(255,255,255,${item.shine}) 50%, ${item.bg} 100%)`,
                  border: idx === 1 ? '4px solid #FBBF24' : '2px solid rgba(255,255,255,0.2)',
                  padding: '22px 14px',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  textAlign: 'center',
                  transform: `translateY(${interpolate(barGrow, [0, 1], [35 + idx * 15, 0])}px)`,
                  opacity: barGrow,
                }}
              >
                <div style={{ color: '#FFFFFF', fontSize: 28, fontWeight: 900 }}>{item.name}</div>
                <div
                  style={{
                    backgroundColor: 'rgba(9,13,22,0.75)',
                    color: '#FBBF24',
                    fontSize: 24,
                    fontWeight: 900,
                    padding: '8px 14px',
                    borderRadius: 12,
                  }}
                >
                  غسيل: {item.wash}
                </div>
                <div style={{ color: '#F8FAFC', fontSize: 22, fontWeight: 700 }}>{item.sub}</div>
              </div>
            ))}
          </div>
        </div>
      );

    case 'wall_layers_xray':
      return (
        <div
          style={{
            width: 960,
            height: 520,
            borderRadius: 28,
            backgroundColor: 'rgba(15, 23, 42, 0.90)',
            border: `3px solid ${scene.accent}`,
            padding: '28px 32px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
          }}
        >
          <div style={{ color: '#FFFFFF', fontSize: 30, fontWeight: 900, textAlign: 'center' }}>
            طبقات التأسيس الهندسي الصحيح للجدار
          </div>
          {[
            { num: '1', label: 'لياسة وصنفرة ميكانيكية وتنظيف الغبار', color: '#64748B', w: '100%' },
            { num: '2', label: 'برايمر عازل مقاوم للرطوبة والقلويات', color: '#0284C7', w: `${Math.round(barGrow * 94)}%` },
            { num: '3', label: 'وجهين معجون أصلية عالية الالتصاق', color: '#D97706', w: `${Math.round(barGrow * 88)}%` },
            { num: '4', label: 'وجهين دهان نهائي مقاوم للغسيل والتبهيت', color: '#16A34A', w: `${Math.round(barGrow * 82)}%` },
          ].map((layer, idx) => (
            <div
              key={idx}
              style={{
                width: layer.w,
                minWidth: 320,
                backgroundColor: layer.color,
                borderRadius: 16,
                padding: '16px 24px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                boxShadow: '0 8px 20px rgba(0,0,0,0.35)',
              }}
            >
              <span style={{ color: '#FFFFFF', fontSize: 26, fontWeight: 900 }}>{layer.label}</span>
              <span
                style={{
                  backgroundColor: 'rgba(0,0,0,0.35)',
                  color: '#FFFFFF',
                  fontSize: 26,
                  fontWeight: 900,
                  width: 44,
                  height: 44,
                  borderRadius: 999,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                {layer.num}
              </span>
            </div>
          ))}
        </div>
      );

    case 'cost_calculator':
      return (
        <div
          style={{
            width: 960,
            height: 520,
            borderRadius: 28,
            backgroundColor: 'rgba(15, 23, 42, 0.90)',
            border: `3px solid ${scene.accent}`,
            padding: '32px 34px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
          }}
        >
          <div style={{ color: '#FBBF24', fontSize: 30, fontWeight: 900, textAlign: 'center' }}>
            مقارنة التكلفة الفعلية على مدى 10 سنوات
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 26 }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#FCA5A5', fontSize: 26, fontWeight: 900, marginBottom: 10 }}>
                <span>دهان تجاري رخيص (إعادة صبغ كل سنتين)</span>
                <span>تكلفة مضاعفة 3x ❌</span>
              </div>
              <div style={{ width: '100%', height: 46, backgroundColor: '#1E293B', borderRadius: 14, overflow: 'hidden' }}>
                <div style={{ width: `${Math.round(barGrow * 96)}%`, height: '100%', backgroundColor: '#DC2626' }} />
              </div>
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#86EFAC', fontSize: 26, fontWeight: 900, marginBottom: 10 }}>
                <span>دهان أصلي + برايمر (محل خيبر للدهانات)</span>
                <span>توفير 35% + ضمان ✅</span>
              </div>
              <div style={{ width: '100%', height: 46, backgroundColor: '#1E293B', borderRadius: 14, overflow: 'hidden' }}>
                <div style={{ width: `${Math.round(barGrow * 58)}%`, height: '100%', backgroundColor: '#16A34A' }} />
              </div>
            </div>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-around', backgroundColor: '#090D16', padding: '18px', borderRadius: 18 }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ color: '#FBBF24', fontSize: 36, fontWeight: 900 }}>+35%</div>
              <div style={{ color: '#CBD5E1', fontSize: 22 }}>تغطية أعلى للمتر</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ color: '#34D399', fontSize: 36, fontWeight: 900 }}>10 سنوات</div>
              <div style={{ color: '#CBD5E1', fontSize: 22 }}>ثبات اللون والجودة</div>
            </div>
          </div>
        </div>
      );

    case 'color_swatches_wall':
      return (
        <div
          style={{
            width: 960,
            height: 520,
            borderRadius: 28,
            backgroundColor: 'rgba(15, 23, 42, 0.90)',
            border: `3px solid ${scene.accent}`,
            padding: '28px 26px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 24px 60px rgba(0,0,0,0.6)',
          }}
        >
          <div style={{ color: '#FFFFFF', fontSize: 30, fontWeight: 900, textAlign: 'center' }}>
            أكثر درجات فلل الرياض طلباً في 2026
          </div>
          <div style={{ display: 'flex', gap: 16, height: 350 }}>
            {[
              { code: 'OW-101', name: 'أبيض لؤلؤي دافئ', hex: '#F5F2EB', text: '#0F172A' },
              { code: 'BG-204', name: 'بيج رملي فاخر', hex: '#E3D5C1', text: '#0F172A' },
              { code: 'GR-308', name: 'جريج مودرن (Greige)', hex: '#C7BFB4', text: '#0F172A' },
              { code: 'ST-412', name: 'حجري خارجي مقاوم', hex: '#9E9384', text: '#FFFFFF' },
            ].map((sw, idx) => (
              <div
                key={idx}
                style={{
                  flex: 1,
                  backgroundColor: sw.hex,
                  borderRadius: 22,
                  padding: '22px 12px',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  textAlign: 'center',
                  border: '3px solid rgba(255,255,255,0.4)',
                  transform: `scale(${interpolate(barGrow, [0, 1], [0.85, 1])})`,
                }}
              >
                <span style={{ backgroundColor: 'rgba(0,0,0,0.18)', color: sw.text, fontSize: 22, fontWeight: 900, padding: '6px 12px', borderRadius: 10 }}>
                  {sw.code}
                </span>
                <span style={{ color: sw.text, fontSize: 25, fontWeight: 900, lineHeight: 1.3 }}>{sw.name}</span>
              </div>
            ))}
          </div>
        </div>
      );

    default:
      // Animated Split-Screen Before vs. After Architectural Wipe
      return (
        <div
          style={{
            width: 960,
            height: 520,
            borderRadius: 28,
            backgroundColor: '#0F172A',
            border: `4px solid ${scene.accent}`,
            position: 'relative',
            overflow: 'hidden',
            boxShadow: '0 24px 60px rgba(0,0,0,0.65)',
          }}
        >
          {/* RIGHT / AFTER: Flawless Luxury Riyadh Wall */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(135deg, #F5EFE6 0%, #E6DCCB 55%, #D6C7B2 100%)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 36,
            }}
          >
            <div
              style={{
                backgroundColor: '#16A34A',
                color: '#FFFFFF',
                fontSize: 30,
                fontWeight: 900,
                padding: '12px 30px',
                borderRadius: 16,
                marginBottom: 16,
              }}
            >
              {scene.rightMetric || 'تشطيب أصلي ناعم بضمان ✅'}
            </div>
            <div style={{ color: '#1E293B', fontSize: 34, fontWeight: 900 }}>
              مقاوم للحرارة والرطوبة والغسيل
            </div>
          </div>

          {/* LEFT / BEFORE: Cracked & Peeling Cheap Wall */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              width: `${wipePct}%`,
              overflow: 'hidden',
              background: 'linear-gradient(135deg, #475569 0%, #334155 100%)',
              borderRight: `6px solid ${scene.accent}`,
            }}
          >
            <svg width="960" height="520" viewBox="0 0 960 520">
              <path d="M 140 90 L 240 210 L 180 340 L 290 450" fill="none" stroke="#FCA5A5" strokeWidth="7" strokeLinecap="round" />
              <path d="M 420 70 L 360 190 L 470 300 L 410 440" fill="none" stroke="#FCA5A5" strokeWidth="7" strokeLinecap="round" />
              <path d="M 190 170 Q 290 140 330 235 Q 250 280 180 245 Z" fill="#991B1B" opacity="0.65" />
              <path d="M 520 210 Q 640 185 680 295 Q 580 345 500 290 Z" fill="#991B1B" opacity="0.65" />
            </svg>
            <div
              style={{
                position: 'absolute',
                bottom: 28,
                right: 28,
                backgroundColor: '#DC2626',
                color: '#FFFFFF',
                fontSize: 28,
                fontWeight: 900,
                padding: '10px 24px',
                borderRadius: 14,
              }}
            >
              {scene.leftMetric || 'تقشر وتشقق سريع ❌'}
            </div>
          </div>
        </div>
      );
  }
};

const ProPaintSceneView: React.FC<{
  scene: ProScene;
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
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 140 } });
  const overallPct = ((index + p) / total) * 100;

  if (scene.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#090D16',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
          overflow: 'hidden',
        }}
      >
        {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
        {scene.video ? (
          <OffthreadVideo
            src={staticFile(scene.video)}
            muted
            style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', opacity: 0.4 }}
          />
        ) : null}
        <AbsoluteFill
          style={{
            background: 'radial-gradient(circle at top, rgba(217,119,6,0.28) 0%, rgba(9,13,22,0.94) 70%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '60px 44px',
            textAlign: 'center',
          }}
        >
          <div
            style={{
              transform: `scale(${pop})`,
              backgroundColor: 'rgba(15, 23, 42, 0.94)',
              border: `4px solid ${scene.accent}`,
              borderRadius: 34,
              padding: '52px 40px',
              width: '100%',
              boxShadow: '0 30px 70px rgba(0, 0, 0, 0.7)',
            }}
          >
            <div
              style={{
                backgroundColor: scene.accent,
                color: '#FFFFFF',
                fontSize: 30,
                fontWeight: 900,
                padding: '12px 32px',
                borderRadius: 999,
                display: 'inline-block',
                marginBottom: 26,
              }}
            >
              {offerText}
            </div>
            <div style={{ color: '#FFFFFF', fontSize: 66, fontWeight: 900, lineHeight: 1.2, marginBottom: 22 }}>
              {shopName}
            </div>
            <div style={{ color: '#CBD5E1', fontSize: 34, fontWeight: 700, lineHeight: 1.45, marginBottom: 38 }}>
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
                boxShadow: '0 16px 38px rgba(22, 163, 74, 0.45)',
                marginBottom: 28,
              }}
            >
              واتساب: {whatsapp}
            </div>
            <div style={{ color: '#F8FAFC', fontSize: 30, fontWeight: 700, lineHeight: 1.45 }}>
              {scene.narration}
            </div>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }

  const words = scene.narration.split(/\s+/).filter(Boolean);
  const activeWordIdx = Math.min(words.length - 1, Math.floor(p * words.length * 1.06));
  const chunkSize = 7;
  const chunkStart = Math.floor(activeWordIdx / chunkSize) * chunkSize;
  const visibleWords = words.slice(chunkStart, chunkStart + chunkSize);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090D16',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
        overflow: 'hidden',
      }}
    >
      {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}

      {/* Real verified paint/interior video background when fetched, otherwise rich architectural studio backdrop */}
      {scene.video ? (
        <OffthreadVideo
          src={staticFile(scene.video)}
          muted
          style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', opacity: 0.55 }}
        />
      ) : (
        <AbsoluteFill
          style={{
            background: `radial-gradient(circle at 20% 20%, ${scene.accent}44 0%, #0F172A 55%, #090D16 100%)`,
          }}
        />
      )}

      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(9,13,22,0.86) 0%, rgba(9,13,22,0.35) 38%, rgba(9,13,22,0.35) 62%, rgba(9,13,22,0.92) 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '70px 48px 86px 48px',
        }}
      >
        {/* Top Hook Header */}
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
              marginBottom: 14,
              boxShadow: '0 10px 25px rgba(0,0,0,0.45)',
            }}
          >
            {scene.stepTag}
          </div>
          <div
            style={{
              color: '#FFFFFF',
              fontSize: 50,
              fontWeight: 900,
              lineHeight: 1.25,
              textShadow: '0 4px 18px rgba(0,0,0,0.85)',
            }}
          >
            {scene.title}
          </div>
        </div>

        {/* Center Architectural Visual Motion Card (Guaranteed Visual Content on Every Single Scene!) */}
        <ArchitecturalVisualCard scene={scene} p={p} frame={frame} />

        {/* Bottom Stat Badge + Synchronized Karaoke Captions */}
        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
          {scene.statBadge ? (
            <div
              style={{
                backgroundColor: 'rgba(15, 23, 42, 0.92)',
                border: `2px solid ${scene.accent}`,
                color: '#FBBF24',
                fontSize: 28,
                fontWeight: 900,
                padding: '9px 28px',
                borderRadius: 16,
              }}
            >
              ✦ {scene.statBadge}
            </div>
          ) : null}

          <div
            style={{
              width: '100%',
              backgroundColor: 'rgba(9, 13, 22, 0.90)',
              borderBottom: `7px solid ${scene.accent}`,
              borderRadius: 24,
              padding: '26px 30px',
              textAlign: 'center',
              boxShadow: '0 20px 50px rgba(0,0,0,0.6)',
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
                      fontSize: 40,
                      fontWeight: 900,
                      lineHeight: 1.32,
                      color: isCurrent ? '#FBBF24' : isSpoken ? '#FFFFFF' : 'rgba(255,255,255,0.52)',
                    }}
                  >
                    {w}
                  </span>
                );
              })}
            </div>
          </div>

          <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: 24, fontWeight: 700 }}>
            {shopName} • الرياض • {whatsapp}
          </div>
        </div>

        {/* Top Progress Bar */}
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 10, backgroundColor: 'rgba(255,255,255,0.18)' }}>
          <div style={{ width: `${overallPct}%`, height: '100%', backgroundColor: scene.accent }} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PaintWhiteboard9x16: React.FC = () => {
  const scenes = (wbData.scenes || []) as ProScene[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#090D16' }}>
      {scenes.map((sc, idx) => {
        const from = offset;
        offset += sc.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={sc.frames}>
            <ProPaintSceneView
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