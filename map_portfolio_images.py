#!/usr/bin/env python3
"""
Django Portfolio Image Organizer
Maps existing images to proper blog posts and projects
"""

import os
import shutil
from pathlib import Path

class PortfolioImageMapper:
    """Map and organize portfolio images"""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.static_dir = self.base_dir / 'static' / 'images'
        self.optimized_dir = self.static_dir / 'optimized'
        
        # Create directory structure
        self.dirs = {
            'profile': self.optimized_dir / 'profile',
            'projects': self.optimized_dir / 'projects', 
            'blog': self.optimized_dir / 'blog',
            'ui': self.optimized_dir / 'ui',
            'social': self.optimized_dir / 'social'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def map_images(self):
        """Map existing images to proper categories"""
        
        # Based on server logs and file names, here's the mapping:
        
        image_mappings = {
            # Profile Images
            'profile-pic.png': {
                'category': 'profile',
                'new_name': 'profile-pic.webp',
                'usage': 'Header navigation',
                'target_size': '50KB'
            },
            'New-Profile-Pic-Gero.jpg': {
                'category': 'profile', 
                'new_name': 'about-pic.webp',
                'usage': 'About page',
                'target_size': '40KB'
            },
            
            # Project Images (from server logs)
            'Projects/Activity Suggestor COVER.png': {
                'category': 'projects',
                'new_name': 'activity-suggestor.webp',
                'usage': 'Activity Suggestor Project',
                'target_size': '80KB'
            },
            'Projects/OpenAI Language Learning Assistant COVER.png': {
                'category': 'projects',
                'new_name': 'openai-assistant.webp', 
                'usage': 'OpenAI Language Learning Assistant',
                'target_size': '120KB'
            },
            'Projects/Best English Resources API COVER.png': {
                'category': 'projects',
                'new_name': 'english-api.webp',
                'usage': 'Best English Resources API',
                'target_size': '90KB'
            },
            'Projects/Goodreads Quotes Scraper COVER.png': {
                'category': 'projects',
                'new_name': 'goodreads-scraper.webp',
                'usage': 'Goodreads Quotes Scraper',
                'target_size': '70KB'
            },
            'Projects/Best English Resources Web COVER.png': {
                'category': 'projects',
                'new_name': 'english-web.webp',
                'usage': 'Best English Resources Web',
                'target_size': '85KB'
            },
            
            # CLI/GUI Tools (should be organized under UI category)
            'Password Manager GUI.png': {
                'category': 'ui',
                'new_name': 'password-manager.webp',
                'usage': 'Password Manager Project',
                'target_size': '100KB'
            },
            "Gero's Quizzler App GUI.png": {
                'category': 'ui',
                'new_name': 'quizzler-app.webp',
                'usage': 'Quizzler App Project',
                'target_size': '80KB'
            },
            'Pomodoro App GUI.png': {
                'category': 'ui',
                'new_name': 'pomodoro-app.webp',
                'usage': 'Pomodoro Timer Project',
                'target_size': '70KB'
            },
            'Create_Wordwalls_From_All_Files_In_Folder CLI.png': {
                'category': 'ui',
                'new_name': 'wordwalls-cli.webp',
                'usage': 'Wordwalls CLI Tool',
                'target_size': '90KB'
            },
            'Dowload_List_Of_Youtube_Videos CLI.png': {
                'category': 'ui',
                'new_name': 'youtube-cli.webp',
                'usage': 'YouTube Videos CLI',
                'target_size': '80KB'
            },
            'Memrise Course Vocabulary Lists to Excel CLI.png': {
                'category': 'ui',
                'new_name': 'memrise-cli.webp',
                'usage': 'Memrise Vocabulary CLI',
                'target_size': '85KB'
            },
            'Student Report Generator Project Cover.png': {
                'category': 'ui',
                'new_name': 'student-report-generator.webp',
                'usage': 'Student Report Generator',
                'target_size': '95KB'
            },
            'Scrape lyrics from Viasona Project Cover New.png': {
                'category': 'ui',
                'new_name': 'viasona-scraper.webp',
                'usage': 'Viasona Lyrics Scraper',
                'target_size': '75KB'
            },
            
            # Social Icons (already optimized)
            'linkedin.png': {
                'category': 'social',
                'new_name': 'linkedin.webp',
                'usage': 'Footer social link',
                'target_size': '2KB'
            },
            'github.png': {
                'category': 'social',
                'new_name': 'github.webp',
                'usage': 'Footer social link',
                'target_size': '2KB'
            },
            'twitter.png': {
                'category': 'social',
                'new_name': 'twitter.webp',
                'usage': 'Footer social link',
                'target_size': '2KB'
            },
            'facebook.png': {
                'category': 'social',
                'new_name': 'facebook.webp',
                'usage': 'Footer social link',
                'target_size': '2KB'
            },
            'instagram.png': {
                'category': 'social',
                'new_name': 'instagram.webp',
                'usage': 'Footer social link',
                'target_size': '2KB'
            }
        }
        
        return image_mappings
    
    def create_missing_blog_images(self):
        """Create placeholder blog images based on server logs"""
        
        # Missing blog images from server logs
        missing_blog_images = {
            'Blog_Post_Rest_Api_Cover_jyIIfYW.png': {
                'title': 'REST API Guide',
                'category': 'blog'
            },
            'Learning_Django_2023_Blog_Post_Cover_3K8VWGI.png': {
                'title': 'Learning Django in 2023',
                'category': 'blog'
            },
            'Qué_Bolá_Python_Episodio_1_Cover.png': {
                'title': 'Qué Bolá Python - Episode 1',
                'category': 'blog'
            },
            'Qué_Bolá_Python_Episodio_2_Cover.png': {
                'title': 'Qué Bolá Python - Episode 2', 
                'category': 'blog'
            },
            'Qué_Bolá_Python_Episodio_3_Cover.png': {
                'title': 'Qué Bolá Python - Episode 3',
                'category': 'blog'
            },
            'Philology_English_Ling_Programming_Blog_Post_Cover_Y1hAxSw.png': {
                'title': 'Philology & Programming',
                'category': 'blog'
            },
            'Languages_Programming_Importance_Cover_Blog_Post_sahoXGk.png': {
                'title': 'Importance of Languages in Programming',
                'category': 'blog'
            }
        }
        
        return missing_blog_images
    
    def generate_optimization_report(self):
        """Generate a report of optimization opportunities"""
        
        mappings = self.map_images()
        
        print("📊 Django Portfolio Image Analysis Report")
        print("=" * 50)
        
        total_current_size = 0
        total_optimized_size = 0
        
        for original, info in mappings.items():
            original_path = self.static_dir / original
            if original_path.exists():
                current_size = original_path.stat().st_size
                total_current_size += current_size
                
                # Estimate optimized size
                target_kb = int(info['target_size'].replace('KB', ''))
                optimized_size = target_kb * 1024
                total_optimized_size += optimized_size
                
                savings = current_size - optimized_size
                savings_percent = (savings / current_size) * 100
                
                print(f"📁 {original}")
                print(f"   Category: {info['category']}")
                print(f"   Usage: {info['usage']}")
                print(f"   Current: {current_size/1024:.1f}KB")
                print(f"   Target: {target_kb}KB")
                print(f"   Savings: {savings/1024:.1f}KB ({savings_percent:.1f}%)")
                print()
        
        total_savings = total_current_size - total_optimized_size
        total_savings_percent = (total_savings / total_current_size) * 100
        
        print("📈 Summary:")
        print(f"   Current Total: {total_current_size/1024/1024:.1f}MB")
        print(f"   Optimized Total: {total_optimized_size/1024/1024:.1f}MB")
        print(f"   Total Savings: {total_savings/1024/1024:.1f}MB ({total_savings_percent:.1f}%)")
        print()
        
        # Check for duplicates
        print("🔍 Duplicate Detection:")
        if (self.static_dir / 'Gero.jpg').exists():
            print("   ⚠️  Found duplicate: Gero.jpg (same as New-Profile-Pic-Gero.jpg)")
        
        # Check for heavy files
        print("🗜️  Heavy Files (>500KB):")
        for file_path in self.static_dir.glob('*.png'):
            if file_path.stat().st_size > 500 * 1024:
                print(f"   ⚠️  {file_path.name}: {file_path.stat().st_size/1024/1024:.1f}MB")
        
        return mappings

if __name__ == "__main__":
    # Run the analysis
    base_dir = "/home/gero/Downloads/Coding/PORTFOLIO_STABLE/gerozayas_portfolio_bravo"
    mapper = PortfolioImageMapper(base_dir)
    
    mappings = mapper.generate_optimization_report()
    missing_blogs = mapper.create_missing_blog_images()
    
    print(f"\n📝 Missing Blog Images: {len(missing_blogs)}")
    for filename, info in missing_blogs.items():
        print(f"   - {info['title']}: {filename}")
    
    print(f"\n🎯 Ready to optimize {len(mappings)} images!")
