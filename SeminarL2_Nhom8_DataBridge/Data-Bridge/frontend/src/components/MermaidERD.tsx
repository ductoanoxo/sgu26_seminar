'use client';

import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { ZoomIn, ZoomOut, RotateCcw, Download, MousePointer2, ChevronDown, FileCode, FileImage, ImageIcon } from 'lucide-react';

interface MermaidERDProps {
  chart: string;
}

type ExportFormat = 'svg' | 'png' | 'jpg';

export default function MermaidERD({ chart }: MermaidERDProps) {
  const svgRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [scale, setScale] = useState(0.8);
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [showExportMenu, setShowExportMenu] = useState(false);
  const exportMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const style = getComputedStyle(document.documentElement);
    const accentPrimary = style.getPropertyValue('--accent-primary').trim() || '#2563eb';
    const bgSecondary = style.getPropertyValue('--bg-secondary').trim() || '#ffffff';
    const bgTertiary = style.getPropertyValue('--bg-tertiary').trim() || '#f1f5f9';

    mermaid.initialize({
      startOnLoad: false,
      theme: 'neutral',
      securityLevel: 'loose',
      fontFamily: "'Inter', sans-serif",
      themeVariables: {
        primaryColor: accentPrimary,
        primaryTextColor: '#ffffff',
        primaryBorderColor: accentPrimary,
        lineColor: accentPrimary,
        secondaryColor: bgTertiary,
        tertiaryColor: bgSecondary,
        mainBkg: bgSecondary,
        nodeBorder: accentPrimary,
        clusterBkg: bgTertiary,
      }
    });

    const handleClickOutside = (e: MouseEvent) => {
      if (exportMenuRef.current && !exportMenuRef.current.contains(e.target as Node)) {
        setShowExportMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (svgRef.current && chart) {
      setError(null);
      const id = `mermaid-erd-${Math.random().toString(36).substr(2, 9)}`;
      
      mermaid.render(id, chart)
        .then(({ svg }) => {
          if (svgRef.current) {
            svgRef.current.innerHTML = svg;
            const svgElement = svgRef.current.querySelector('svg');
            if (svgElement) {
              svgElement.style.maxWidth = '100%';
              svgElement.style.height = 'auto';
              
              const style = getComputedStyle(document.documentElement);
              const accentPrimary = style.getPropertyValue('--accent-primary').trim() || '#2563eb';
              const textPrimary = style.getPropertyValue('--text-primary').trim() || '#0f172a';
              const bgSecondary = style.getPropertyValue('--bg-secondary').trim() || '#ffffff';
              const borderPrimary = style.getPropertyValue('--border-primary').trim() || '#e2e8f0';

              const styleTag = document.createElementNS("http://www.w3.org/2000/svg", "style");
              styleTag.textContent = `
                .er.entityBox { fill: ${accentPrimary} !important; stroke: ${accentPrimary} !important; rx: 10px; ry: 10px; }
                .er.entityLabel { fill: #ffffff !important; font-weight: 700 !important; font-size: 15px !important; }
                .er.attributeBoxEven, .er.attributeBoxOdd { fill: ${bgSecondary} !important; stroke: ${borderPrimary} !important; stroke-width: 0.5px !important; }
                .er.attributeLabel { fill: ${textPrimary} !important; font-size: 13px !important; font-weight: 400 !important; }
                .er.relationshipLine { stroke: ${accentPrimary} !important; stroke-width: 2px !important; opacity: 0.8; }
                .er.relationshipLabel { fill: ${textPrimary} !important; font-weight: 600 !important; font-size: 11px !important; }
                .er.relationshipLabelRect { fill: ${bgSecondary} !important; fill-opacity: 0.9 !important; rx: 4px; }
                text { font-family: 'Inter', system-ui, sans-serif !important; }
              `;
              svgElement.prepend(styleTag);
            }
          }
        })
        .catch((e) => {
          console.error("Mermaid render error:", e);
          setError("Failed to render diagram. Please check your schema.");
        });
    }
  }, [chart]);

  const exportAsImage = async (format: ExportFormat) => {
    if (!svgRef.current) return;
    const svgElement = svgRef.current.querySelector('svg');
    if (!svgElement) return;

    // Get the actual content size from viewBox or BBox
    const viewBox = svgElement.viewBox.baseVal;
    const width = viewBox.width > 0 ? viewBox.width : svgElement.getBBox().width;
    const height = viewBox.height > 0 ? viewBox.height : svgElement.getBBox().height;
    const xOffset = viewBox.x || 0;
    const yOffset = viewBox.y || 0;

    if (format === 'svg') {
      const svgData = svgRef.current.innerHTML;
      const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'database-erd.svg';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setShowExportMenu(false);
      return;
    }

    // Clone and prepare SVG for rasterization
    const clonedSvg = svgElement.cloneNode(true) as SVGSVGElement;
    clonedSvg.setAttribute('width', width.toString());
    clonedSvg.setAttribute('height', height.toString());
    
    const svgData = new XMLSerializer().serializeToString(clonedSvg);
    const svgBase64 = btoa(unescape(encodeURIComponent(svgData)));
    const svgDataUrl = `data:image/svg+xml;base64,${svgBase64}`;
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    // Set high quality scale (3x)
    const scaleFactor = 3;
    const padding = 40;
    canvas.width = (width + padding * 2) * scaleFactor;
    canvas.height = (height + padding * 2) * scaleFactor;
    
    img.onload = () => {
      if (!ctx) return;
      
      try {
        // Fill background
        ctx.fillStyle = format === 'jpg' ? '#ffffff' : 'transparent';
        if (format === 'jpg') {
          ctx.fillRect(0, 0, canvas.width, canvas.height);
        } else {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        
        ctx.scale(scaleFactor, scaleFactor);
        // Draw with padding and compensate for viewBox offset
        ctx.drawImage(img, padding - xOffset, padding - yOffset);
        
        const imageUrl = canvas.toDataURL(format === 'png' ? 'image/png' : 'image/jpeg', 0.95);
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = `database-erd.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setShowExportMenu(false);
      } catch (err) {
        console.error("Export error:", err);
        setError("Could not export image. Please try SVG format.");
        setShowExportMenu(false);
      }
    };
    
    img.src = svgDataUrl;
  };

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.15, 4));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.15, 0.2));
  const handleReset = () => {
    setScale(0.8);
    setPosition({ x: 0, y: 0 });
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    if (e.ctrlKey) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setScale(prev => Math.min(Math.max(prev + delta, 0.2), 4));
    }
  };

  if (error) {
    return <div style={{ color: 'var(--accent-error)', padding: '24px', textAlign: 'center', background: 'var(--bg-secondary)', borderRadius: '12px', border: '1px solid var(--border-primary)' }}>{error}</div>;
  }

  return (
    <div 
      className="erd-canvas-container"
      style={{
        position: 'relative',
        width: '100%',
        height: '600px',
        background: 'var(--bg-secondary)', 
        backgroundImage: `radial-gradient(circle, var(--border-primary) 1px, transparent 1px)`,
        backgroundSize: '24px 24px',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-primary)',
        overflow: 'hidden',
        cursor: isDragging ? 'grabbing' : 'crosshair',
      }}
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* Controls */}
      <div style={{
        position: 'absolute',
        top: '16px',
        right: '16px',
        zIndex: 10,
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
        background: 'var(--bg-secondary)',
        padding: '6px',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-primary)',
        boxShadow: 'var(--shadow-md)',
        backdropFilter: 'blur(8px)'
      }}>
        <button onClick={handleZoomIn} title="Zoom In" style={controlBtnStyle}><ZoomIn size={18} /></button>
        <button onClick={handleZoomOut} title="Zoom Out" style={controlBtnStyle}><ZoomOut size={18} /></button>
        <button onClick={handleReset} title="Reset View" style={controlBtnStyle}><RotateCcw size={18} /></button>
        <div style={{ height: '1px', background: 'var(--border-primary)', margin: '4px 6px' }} />
        
        {/* Export Dropdown */}
        <div style={{ position: 'relative' }} ref={exportMenuRef}>
          <button 
            onClick={() => setShowExportMenu(!showExportMenu)} 
            title="Export ERD" 
            style={{...controlBtnStyle, background: showExportMenu ? 'var(--bg-tertiary)' : 'transparent'}}
          >
            <Download size={18} />
          </button>
          
          {showExportMenu && (
            <div style={{
              position: 'absolute',
              right: 'calc(100% + 12px)',
              top: 0,
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-primary)',
              borderRadius: 'var(--radius-md)',
              boxShadow: 'var(--shadow-lg)',
              minWidth: '140px',
              overflow: 'hidden',
              animation: 'fadeInUp 0.2s ease-out'
            }}>
              <button onClick={() => exportAsImage('svg')} style={menuItemStyle}>
                <FileCode size={14} /> SVG (Vector)
              </button>
              <button onClick={() => exportAsImage('png')} style={menuItemStyle}>
                <FileImage size={14} /> PNG Image
              </button>
              <button onClick={() => exportAsImage('jpg')} style={menuItemStyle}>
                <ImageIcon size={14} /> JPG Image
              </button>
            </div>
          )}
        </div>

        <div style={{ padding: '6px 0', fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center', fontWeight: '800', fontFamily: 'monospace' }}>
          {Math.round(scale * 100)}%
        </div>
      </div>

      {/* Floating Status Label */}
      <div style={{
        position: 'absolute',
        top: '16px',
        left: '16px',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        background: 'var(--bg-secondary)',
        padding: '6px 14px',
        borderRadius: 'var(--radius-full)',
        border: '1px solid var(--border-primary)',
        boxShadow: 'var(--shadow-sm)',
        fontSize: '11px',
        fontWeight: '600',
        color: 'var(--text-secondary)'
      }}>
        <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--accent-primary)' }} />
        Schema Visualization
      </div>

      {/* Navigation Hint */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 5,
        fontSize: '11px',
        color: 'var(--text-muted)',
        background: 'var(--bg-secondary)',
        padding: '8px 20px',
        borderRadius: 'var(--radius-full)',
        border: '1px solid var(--border-primary)',
        boxShadow: 'var(--shadow-lg)',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        whiteSpace: 'nowrap'
      }}>
        <MousePointer2 size={12} style={{ color: 'var(--accent-primary)' }} />
        <span>Kéo để di chuyển · <kbd style={{ background: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px', border: '1px solid var(--border-primary)', fontSize: '10px' }}>Ctrl</kbd> + Cuộn để phóng to</span>
      </div>

      {/* Diagram Canvas */}
      <div 
        ref={svgRef}
        style={{ 
          width: '100%',
          height: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
          transformOrigin: 'center',
          transition: isDragging ? 'none' : 'transform 0.25s cubic-bezier(0.2, 0, 0.2, 1)',
        }}
      />
    </div>
  );
}

const controlBtnStyle: React.CSSProperties = {
  background: 'transparent',
  border: 'none',
  color: 'var(--text-secondary)',
  cursor: 'pointer',
  padding: '8px',
  borderRadius: 'var(--radius-sm)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'all 0.15s'
};

const menuItemStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  width: '100%',
  padding: '10px 16px',
  border: 'none',
  background: 'transparent',
  color: 'var(--text-primary)',
  fontSize: '12px',
  fontWeight: 500,
  textAlign: 'left',
  cursor: 'pointer',
  transition: 'background 0.2s'
};
