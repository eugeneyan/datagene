class AddUserToGames < ActiveRecord::Migration
  def change
  	remove_column :games, :user_id
    add_reference :games, :user, index: true
  end
end
