require 'csv'

class Game < ActiveRecord::Base
	belongs_to :user
	validates_presence_of :user
	validates_presence_of :version
	validates_presence_of :result
	validates_presence_of :game_type


	def skills_for (options={})
		game_type = options[:game_type]
		value = options[:value]

		hash = Array.new
		self.result_hash.each { |k, v|
			skill = Skill.find(k)
			axis = Axis.where({game_type: 1, value: v}).first
			hash << skill if axis.value == value
		}
		hash
	end


	# This method writes a CSV file of one game result
	def populateResult!
		filename = 'game_result.csv'
		file = File.new(Rails.public_path.to_s+"/#{filename}", 'w')
		begin	
			self.result_hash.each { |k, v|
				skill = Skill.find(k)
				axis = Axis.find(v)
				file.puts "#{k},\"#{skill.name}\",#{axis.name}"
			}
			file.close
		rescue Exception => e
			STDERR.puts "Error with file write: #{e}"
			file.close
		end
	end


	# This method write a CSV file of all game results
	def self.allResults!

		filename = 'game_all_results.csv'
		file = File.new(Rails.public_path.to_s+"/#{filename}", 'w')

		begin
			# Print file headers
			header = "id,"
			(1..49).each { |i| header += "#{i},"}
			header += "50"
			file.puts "#{header}"

			# Get all games, for each game, print user and value
			self.all.each { |g|

				result = g.user_id.to_s + ","

				g.result_hash.each { |k,v|
					# skill = Skill.find(k)
					axis = Axis.find(v)
					result += "#{axis.value},"
				}

				file.puts result
			}
			file.close
		rescue Exception => e
			STDERR.puts "Error with file write: #{e}"
			file.close
		end
	end


	def result_hash
		result_hash = Hash.new
		self.result.split(';').each do |pair|
			split_pair = pair.split(',')
			result_hash[split_pair[0].to_i] = split_pair[1].to_i
		end
		result_hash
	end
end
