require 'Nokogiri'
require 'feedjira'
require 'httparty'
require 'jekyll'

module ExternalPublications
  class ExternalPublicationsGenerator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      if site.config['publications_sources'] != nil
        real_category_names = ['All', 'Article', 'Letter', 'Review Article', 'Chapter', 'Comment/Debate', 'Conference Contribution', 'Conference Article', 'Poster', 'Editorial', 'Meeting Abstract', 'Short Survey', 'Preprint', 'Working Paper', 'Web Publication/site', 'Patent', 'Entry for encyclopedia/dictionary', 'Special Issue', 'Data set/Database', 'Commissioned Report', 'Book', 'Other Contribution', 'Doctoral Thesis' ] 
        site.config['publications_sources'].each do |src|
          p "Fetching external Publications from #{src['name']}:"
          xml = HTTParty.get(src['rss_url']).body
          feed = Feedjira.parse(xml)
          feed.entries.each do |e|
            slug = e.title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
            path = site.in_source_dir("_posts/#{slug}.md")
            
            # Parsing the publication to extract its category
            parsed = Nokogiri::HTML5(e.summary)
            temp = parsed.css("span.type_classification")
            if temp.count > 0
               category = temp[0].children[0].text
            else
               temp = parsed.css("span.type_classification_parent")
               if temp.count > 0
                 category = temp[0].children[0].text
               else
                 category = "Other"
               end
            end
            
            
            doc = Jekyll::Document.new(
              path, { :site => site, :collection => site.collections['publications'] }
            )
            doc.data['external_source'] = src['name'];
            doc.data['feed_content'] = e.content;
            doc.data['title'] = "#{e.title}";
            doc.data['description'] = e.summary;
            doc.data['date'] = e.published;
            doc.data['year'] = e.published.year;
            doc.data['redirect'] = e.url;
            doc.data['category'] = category;
            
            # Keep only the requested categories items
            selected_cetegories = site.config['publications_categories']
			plural_category = ""
            selected_cetegories.each do |cat|
               case category.downcase
               when "article"
                 plural_category = "Articles"
               when "letter"
                 plural_category = "Letters"
               when "review article"
                 plural_category = "Review Articles"
               when "chapter"
                 plural_category = "Chapters"
               when "comment/debate"
                 plural_category = "Comments/Debates"
               when 'conference contribution'
                 plural_category = 'Conference Contributions'
               when 'conference article'
                 plural_category = 'Conference Articles'
               when 'poster'
                 plural_category = 'Posters'
               when 'editorial'
                 plural_category = 'Editorials'
               when 'meeting abstract'
                 plural_category = 'Meeting Abstracts'
               when 'short survey'
                 plural_category = 'Short Surveys'
               when 'preprint'
                 plural_category = 'Preprints'
               when 'working paper'
                 plural_category = 'Working Papers'
               when 'web publication/site'
                 plural_category = 'Web Publications/sites'
               when 'anthology'
                 plural_category = 'Anthologies'
               when 'patent'
                 plural_category = 'Patents'
               when 'entry for encyclopedia/dictionary'
                 plural_category = 'Entries for encyclopedia/dictionary'
               when 'special issue'
                 plural_category = 'Special Issues'
               when 'data set/database'
                 plural_category = 'Data sets/Databases'
               when 'commissioned report'
                 plural_category = 'Commissioned Reports'
               when 'book'
                 plural_category = 'Books'
               when 'other contribution'
                 plural_category = 'Other Contributions'
               when 'doctoral thesis'
                 plural_category = 'Doctoral Thesises'
               when 'other'
                 plural_category = 'Other'
               end
            end
            
			doc.data['plural_category'] = plural_category;
			
            if selected_cetegories.include?(plural_category) or category = "Other"
              site.collections['publications'].docs << doc
            end

          end
        end
      end
    end
  end

end

