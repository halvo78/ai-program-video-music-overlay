# Taj Chat - Quick Reference Guide

## 🚀 Quick Start

### Video Wall Component
**Location:** `dashboard/app/page.tsx`

### Key Components
- `VideoWall()` - Main video wall container
- `VideoCard()` - Individual video card with hover playback

### Current Video Configuration
```javascript
const videos = [
  {
    thumbnail: 'URL',        // 9:16 aspect ratio image
    video: 'URL',            // Video file URL
    startTime: 5,            // Seconds - matches thumbnail frame
    title: 'Title',
    category: 'Category',
    views: 'X.XM',
    duration: '0:XX',
    platform: 'Platform'
  }
]
```

## 🔧 Key Features

### Video Playback
- ✅ Hover to play
- ✅ Starts from thumbnail frame
- ✅ Sound at 40% volume
- ✅ Smooth transitions

### Design
- ✅ InVideo-inspired
- ✅ Professional blue palette
- ✅ 9:16 aspect ratio
- ✅ Responsive grid

## 📝 Common Tasks

### Add New Video
1. Add object to `videos` array
2. Set `startTime` to match thumbnail
3. Ensure 9:16 aspect ratio

### Adjust Start Time
1. Find frame in video matching thumbnail
2. Update `startTime` property
3. Test hover playback

### Change Design
- Colors: `globals.css`
- Layout: `page.tsx` VideoWall component
- Styling: Tailwind classes in components

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Video not playing | Check URL, format, CORS |
| Thumbnail mismatch | Adjust `startTime` |
| Aspect ratio wrong | Use 9:16 (400x711) |
| No hover effect | Check `isHovered` state |

## 📂 File Locations

- Main component: `dashboard/app/page.tsx`
- Styles: `dashboard/app/globals.css`
- Layout: `dashboard/app/layout.tsx`
- Components: `dashboard/app/components/`

## 🎯 Current State

- **Videos:** 8 configured
- **Status:** Production-ready
- **Next:** Replace sample videos with real content
