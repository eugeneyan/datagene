class CreateGames < ActiveRecord::Migration
  def change
    create_table :games do |t|
      t.integer :user_id
      t.string :version
      t.text :result

      t.timestamps
    end
  end
end
