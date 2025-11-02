#!/usr/bin/env python3
"""
Performance Monitoring Script for Django Portfolio
Measures image optimization results and Core Web Vitals
"""

import os
import time
import requests
from pathlib import Path
from PIL import Image

class PerformanceMonitor:
    """Monitor portfolio performance after optimization"""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.static_dir = self.base_dir / 'static' / 'images'
        self.optimized_dir = self.static_dir / 'optimized'
    
    def measure_image_sizes(self):
        """Compare original vs optimized image sizes"""
        
        print("📊 Image Size Comparison Report")
        print("=" * 50)
        
        original_total = 0
        optimized_total = 0
        
        # Check profile images
        profile_original = self.static_dir / 'profile-pic.png'
        profile_optimized = self.optimized_dir / 'profile' / 'profile-pic.jpg'
        
        if profile_original.exists() and profile_optimized.exists():
            orig_size = profile_original.stat().st_size
            opt_size = profile_optimized.stat().st_size
            savings = orig_size - opt_size
            savings_percent = (savings / orig_size) * 100
            
            print(f"👤 Profile Picture:")
            print(f"   Original: {orig_size/1024:.1f}KB")
            print(f"   Optimized: {opt_size/1024:.1f}KB")
            print(f"   Savings: {savings/1024:.1f}KB ({savings_percent:.1f}%)")
            print()
            
            original_total += orig_size
            optimized_total += opt_size
        
        # Check project images
        print("🚀 Project Images:")
        project_files = [
            ('Activity Suggestor COVER.png', 'activity-suggestor.jpg'),
            ('OpenAI Language Learning Assistant COVER.png', 'openai-assistant.jpg'),
            ('Best English Resources API COVER.png', 'english-api.jpg'),
            ('Goodreads Quotes Scraper COVER.png', 'goodreads-scraper.jpg'),
            ('Best English Resources Web COVER.png', 'english-web.jpg'),
        ]
        
        for original_file, optimized_file in project_files:
            orig_path = self.static_dir / 'Projects' / original_file
            opt_path = self.optimized_dir / 'projects' / optimized_file
            
            if orig_path.exists() and opt_path.exists():
                orig_size = orig_path.stat().st_size
                opt_size = opt_path.stat().st_size
                savings = orig_size - opt_size
                savings_percent = (savings / orig_size) * 100
                
                print(f"   {optimized_file.replace('-', ' ').title()}:")
                print(f"     Original: {orig_size/1024:.1f}KB")
                print(f"     Optimized: {opt_size/1024:.1f}KB")
                print(f"     Savings: {savings/1024:.1f}KB ({savings_percent:.1f}%)")
                
                original_total += orig_size
                optimized_total += opt_size
        
        print()
        
        # Check blog images (newly created)
        blog_dir = self.optimized_dir / 'blog'
        if blog_dir.exists():
            blog_files = list(blog_dir.glob('*.jpg'))
            blog_size = sum(f.stat().st_size for f in blog_files)
            print(f"📝 Blog Images (NEW):")
            print(f"   Total: {blog_size/1024:.1f}KB ({len(blog_files)} files)")
            optimized_total += blog_size
        
        print()
        print("📈 Summary:")
        print(f"   Original Total: {original_total/1024/1024:.1f}MB")
        print(f"   Optimized Total: {optimized_total/1024/1024:.1f}MB")
        
        if original_total > 0:
            total_savings = original_total - optimized_total
            total_savings_percent = (total_savings / original_total) * 100
            print(f"   Total Savings: {total_savings/1024/1024:.1f}MB ({total_savings_percent:.1f}%)")
        
        return {
            'original_mb': original_total / 1024 / 1024,
            'optimized_mb': optimized_total / 1024 / 1024,
            'savings_mb': (original_total - optimized_total) / 1024 / 1024
        }
    
    def check_webp_support(self):
        """Check WebP files were created successfully"""
        
        print("\n🌐 WebP Format Support:")
        print("=" * 30)
        
        webp_files = list(self.optimized_dir.rglob('*.webp'))
        total_webp_size = sum(f.stat().st_size for f in webp_files)
        
        print(f"WebP files created: {len(webp_files)}")
        print(f"Total WebP size: {total_webp_size/1024:.1f}KB")
        
        if webp_files:
            avg_compression = 0
            count = 0
            
            for webp_file in webp_files:
                jpg_file = webp_file.with_suffix('.jpg')
                if jpg_file.exists():
                    webp_size = webp_file.stat().st_size
                    jpg_size = jpg_file.stat().st_size
                    compression = ((jpg_size - webp_size) / jpg_size) * 100
                    avg_compression += compression
                    count += 1
            
            if count > 0:
                avg_compression /= count
                print(f"Average WebP compression: {avg_compression:.1f}%")
        
        return len(webp_files)
    
    def analyze_image_quality(self):
        """Analyze image quality metrics"""
        
        print("\n🎨 Image Quality Analysis:")
        print("=" * 35)
        
        quality_metrics = {}
        
        # Check a few sample images
        sample_images = [
            ('profile/profile-pic.jpg', 'Profile Picture'),
            ('projects/openai-assistant.jpg', 'OpenAI Assistant'),
            ('blog/Learning_Django_2023_Blog_Post_Cover_3K8VWGI.jpg', 'Django Blog Cover')
        ]
        
        for img_path, img_name in sample_images:
            full_path = self.optimized_dir / img_path
            if full_path.exists():
                try:
                    with Image.open(full_path) as img:
                        width, height = img.size
                        mode = img.mode
                        format_name = img.format
                        
                        print(f"📸 {img_name}:")
                        print(f"   Dimensions: {width}x{height}")
                        print(f"   Color mode: {mode}")
                        print(f"   Format: {format_name}")
                        
                        quality_metrics[img_name] = {
                            'dimensions': f"{width}x{height}",
                            'mode': mode,
                            'format': format_name
                        }
                except Exception as e:
                    print(f"❌ Error analyzing {img_name}: {e}")
        
        return quality_metrics
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        
        print("🚀 Django Portfolio Performance Report")
        print("=" * 50)
        print(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Measure image sizes
        size_metrics = self.measure_image_sizes()
        
        # Check WebP support
        webp_count = self.check_webp_support()
        
        # Analyze quality
        quality_metrics = self.analyze_image_quality()
        
        # Performance recommendations
        print("\n💡 Performance Recommendations:")
        print("=" * 40)
        
        if size_metrics['savings_mb'] > 1:
            print("✅ Excellent image optimization achieved!")
            print(f"   • Saved {size_metrics['savings_mb']:.1f}MB in image size")
            print("   • Faster page loads expected")
            print("   • Better Core Web Vitals scores")
        
        if webp_count > 5:
            print("✅ WebP format successfully implemented")
            print("   • Modern browsers will load faster")
            print("   • Bandwidth usage reduced")
        
        print("\n🎯 Next Steps:")
        print("1. Test website loading speed")
        print("2. Monitor Core Web Vitals in Google Search Console")
        print("3. Check mobile performance")
        print("4. Set up CDN for static files")
        print("5. Enable browser caching headers")
        
        return {
            'size_metrics': size_metrics,
            'webp_files': webp_count,
            'quality_metrics': quality_metrics
        }

if __name__ == "__main__":
    base_dir = "/home/gero/Downloads/Coding/PORTFOLIO_STABLE/gerozayas_portfolio_bravo"
    monitor = PerformanceMonitor(base_dir)
    
    report = monitor.generate_performance_report()
    
    print(f"\n✅ Performance analysis complete!")
    print(f"📊 Ready to monitor improvements!")
