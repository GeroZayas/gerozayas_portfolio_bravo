#!/bin/bash

# Django Portfolio Image Optimization Script
# Execute this to optimize all images and fix missing ones

echo "🚀 Starting Django Portfolio Image Optimization..."
echo "=================================================="

# Set base directory
BASE_DIR="/home/gero/Downloads/Coding/PORTFOLIO_STABLE/gerozayas_portfolio_bravo"
STATIC_DIR="$BASE_DIR/static/images"
OPTIMIZED_DIR="$STATIC_DIR/optimized"

# Create directory structure
echo "📁 Creating optimized directory structure..."
mkdir -p "$OPTIMIZED_DIR"/{profile,projects,blog,ui,social,assets}

# Install optimization tools if not available
echo "🔧 Checking for optimization tools..."
if ! command -v optipng &> /dev/null; then
    echo "⚠️  optipng not found. Install with: sudo apt-get install optipng"
fi

if ! command -v jpegoptim &> /dev/null; then
    echo "⚠️  jpegoptim not found. Install with: sudo apt-get install jpegoptim"
fi

if ! command -v convert &> /dev/null; then
    echo "⚠️  ImageMagick not found. Install with: sudo apt-get install imagemagick"
fi

# Function to optimize image
optimize_image() {
    local input="$1"
    local output="$2"
    local max_size_kb="$3"
    local quality="$4"
    
    if [[ ! -f "$input" ]]; then
        echo "❌ Input file not found: $input"
        return 1
    fi
    
    echo "📸 Optimizing: $(basename "$input")"
    
    # Get original size
    original_size=$(stat -f%z "$input" 2>/dev/null || stat -c%s "$input")
    
    # Convert to WebP with fallback
    if command -v cwebp &> /dev/null; then
        # Use cwebp for WebP conversion
        cwebp -q "$quality" "$input" -o "${output%.webp}.webp" 2>/dev/null
    else
        # Use ImageMagick as fallback
        convert "$input" -quality "$quality" -strip "${output%.webp}.webp" 2>/dev/null
    fi
    
    # Check if WebP was created and is within size limit
    webp_output="${output%.webp}.webp"
    if [[ -f "$webp_output" ]]; then
        webp_size=$(stat -f%z "$webp_output" 2>/dev/null || stat -c%s "$webp_output")
        webp_size_kb=$((webp_size / 1024))
        
        if [[ $webp_size_kb -le $max_size_kb ]]; then
            echo "   ✅ WebP: ${webp_size_kb}KB (saved $(( (original_size - webp_size) / 1024 ))KB)"
        else
            echo "   ⚠️  WebP too large: ${webp_size_kb}KB (target: ${max_size_kb}KB)"
            # Try lower quality
            for q in $(seq $((quality - 10)) 50 -10); do
                convert "$input" -quality "$q" -strip "$webp_output"
                webp_size=$(stat -f%z "$webp_output" 2>/dev/null || stat -c%s "$webp_output")
                webp_size_kb=$((webp_size / 1024))
                if [[ $webp_size_kb -le $max_size_kb ]]; then
                    echo "   ✅ WebP (quality $q): ${webp_size_kb}KB"
                    break
                fi
            done
        fi
    fi
    
    # Create JPEG fallback
    if [[ "$input" == *.jpg || "$input" == *.jpeg ]]; then
        if command -v jpegoptim &> /dev/null; then
            jpegoptim --max="$quality" --strip-all --outfile="$output" "$input"
        else
            convert "$input" -quality "$quality" -strip "$output"
        fi
    else
        # Convert PNG to JPEG fallback
        convert "$input" -background white -alpha remove -quality "$quality" -strip "$output"
    fi
    
    # Get final sizes
    if [[ -f "$output" ]]; then
        final_size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output")
        echo "   ✅ JPEG: $((final_size / 1024))KB (saved $(( (original_size - final_size) / 1024 ))KB)"
    fi
}

# Remove duplicates and heavy files
echo "🗑️  Cleaning up duplicates and heavy files..."
cd "$STATIC_DIR"

# Remove duplicate profile image
if [[ -f "Gero.jpg" ]]; then
    echo "   Removing duplicate: Gero.jpg ($(stat -c%s "Gero.jpg" | awk '{print $1/1024/1024 "MB"}'))"
    rm "Gero.jpg"
fi

# Remove heavy unused images (3MB each)
heavy_files=("img-7Pp9vNI7GthikYjzLsdsmSrP.png" "img-iotbizNNTihDsW4cQPcCW8qm.png")
for file in "${heavy_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "   Removing heavy file: $file ($(stat -c%s "$file" | awk '{print $1/1024/1024 "MB"}'))"
        rm "$file"
    fi
done

# Optimize profile images
echo "👤 Optimizing profile images..."
optimize_image "$STATIC_DIR/profile-pic.png" "$OPTIMIZED_DIR/profile/profile-pic.jpg" 50 85
optimize_image "$STATIC_DIR/New-Profile-Pic-Gero.jpg" "$OPTIMIZED_DIR/profile/about-pic.jpg" 40 85

# Optimize project images
echo "🚀 Optimizing project images..."
optimize_image "$STATIC_DIR/Projects/Activity Suggestor COVER.png" "$OPTIMIZED_DIR/projects/activity-suggestor.jpg" 80 80
optimize_image "$STATIC_DIR/Projects/OpenAI Language Learning Assistant COVER.png" "$OPTIMIZED_DIR/projects/openai-assistant.jpg" 120 85
optimize_image "$STATIC_DIR/Projects/Best English Resources API COVER.png" "$OPTIMIZED_DIR/projects/english-api.jpg" 90 80
optimize_image "$STATIC_DIR/Projects/Goodreads Quotes Scraper COVER.png" "$OPTIMIZED_DIR/projects/goodreads-scraper.jpg" 70 80
optimize_image "$STATIC_DIR/Projects/Best English Resources Web COVER.png" "$OPTIMIZED_DIR/projects/english-web.jpg" 85 80

# Optimize UI/CLI images
echo "💻 Optimizing UI/CLI images..."
optimize_image "$STATIC_DIR/Password Manager GUI.png" "$OPTIMIZED_DIR/ui/password-manager.jpg" 100 85
optimize_image "$STATIC_DIR/Gero's Quizzler App GUI.png" "$OPTIMIZED_DIR/ui/quizzler-app.jpg" 80 85
optimize_image "$STATIC_DIR/Pomodoro App GUI.png" "$OPTIMIZED_DIR/ui/pomodoro-app.jpg" 70 85
optimize_image "$STATIC_DIR/Create_Wordwalls_From_All_Files_In_Folder CLI.png" "$OPTIMIZED_DIR/ui/wordwalls-cli.jpg" 90 80
optimize_image "$STATIC_DIR/Dowload_List_Of_Youtube_Videos CLI.png" "$OPTIMIZED_DIR/ui/youtube-cli.jpg" 80 80
optimize_image "$STATIC_DIR/Memrise Course Vocabulary Lists to Excel CLI.png" "$OPTIMIZED_DIR/ui/memrise-cli.jpg" 85 80
optimize_image "$STATIC_DIR/Student Report Generator Project Cover.png" "$OPTIMIZED_DIR/ui/student-report-generator.jpg" 95 85
optimize_image "$STATIC_DIR/Scrape lyrics from Viasona Project Cover New.png" "$OPTIMIZED_DIR/ui/viasona-scraper.jpg" 75 80

# Optimize social icons
echo "🔗 Optimizing social icons..."
for icon in linkedin github twitter facebook instagram; do
    optimize_image "$STATIC_DIR/${icon}.png" "$OPTIMIZED_DIR/social/${icon}.jpg" 2 90
done

# Create placeholder blog images
echo "📝 Creating placeholder blog images..."
blog_posts=(
    "Blog_Post_Rest_Api_Cover_jyIIfYW.png:REST API Guide"
    "Learning_Django_2023_Blog_Post_Cover_3K8VWGI.png:Learning Django in 2023"
    "Qu_Bol_Python_Episodio_1_Cover.png:Qué Bolá Python - Episode 1"
    "Qu_Bol_Python_Episodio_2_Cover.png:Qué Bolá Python - Episode 2"
    "Qu_Bol_Python_Episodio_3_Cover.png:Qué Bolá Python - Episode 3"
    "Philology_English_Ling_Programming_Blog_Post_Cover_Y1hAxSw.png:Philology & Programming"
    "Languages_Programming_Importance_Cover_Blog_Post_sahoXGk.png:Importance of Languages in Programming"
)

for post_info in "${blog_posts[@]}"; do
    IFS=':' read -r filename title <<< "$post_info"
    echo "   Creating placeholder for: $title"
    
    # Create a simple gradient placeholder
    convert -size 800x400 xc:"#2a9d8f" \
            -font DejaVu-Sans-Bold -pointsize 48 -fill white -gravity center \
            -annotate +0+0 "$title" \
            -quality 80 -strip "$OPTIMIZED_DIR/blog/${filename%.png}.jpg"
done

# Calculate final statistics
echo ""
echo "📊 Optimization Results:"
echo "========================"

original_total=$(find "$STATIC_DIR" -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | xargs du -ch | grep total | cut -f1)
optimized_total=$(find "$OPTIMIZED_DIR" -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | xargs du -ch | grep total | cut -f1)

echo "Original size: $original_total"
echo "Optimized size: $optimized_total"
echo "Files organized: $(find "$OPTIMIZED_DIR" -type f | wc -l)"
echo "Blog placeholders created: ${#blog_posts[@]}"

echo ""
echo "🎯 Next Steps:"
echo "1. Update Django templates to use new optimized paths"
echo "2. Run 'python manage.py collectstatic --noinput'"
echo "3. Test all images are loading correctly"
echo "4. Monitor Core Web Vitals improvement"

echo ""
echo "✅ Image optimization complete!"
