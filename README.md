# Python sitemap generator

## Usage
* change url and file path in script
```py
generate = Generate("https://google.com", "path/to/sitemap.xml")
```

## Output example
```xml
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>https://listed.to/@DieSieben/7851/api-des-deutschen-wetterdienstes</loc>
		<lastmod>2024-03-15</lastmod>
		<priority>0.5</priority>
	</url>
</urlset>
```

## Upcoming features
* passing the URL in the command
* analyze URLs and set priority automatically