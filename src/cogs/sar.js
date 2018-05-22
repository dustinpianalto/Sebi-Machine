const Discord = require("discord.js");

exports.run = async function(client, message, args) {

    /*
        aliases: sar, selfrole, selfroles

        examples: 
        - S!selfrole get 1 (adds async helper role)
        - S!sar remove 4 (removes rewrite helper role)
        - S!sar list (shows all roles)
    */

    function roleFinder(query) {
        return message.guild.roles.find(function(r) {
            return r.name.includes(query)
        }).id;
    }

    const type = args[0]; // can be get, remove or list

    if (type == "list") {

        const embed = new Discord.RichEmbed()
            .setTitle("List of Self Assigned Roles")
            .setDescription("Usage: `S!sar [ get | remove | list ] [ number ]`")
            .addField("1. Async Helper", "S!sar get 1", true)
            .addField("2. Heroku Helper", "S!sar get 2", true)
            .addField("3. JS Helper", "S!sar get 3", true)
            .addField("4. Rewrite Helper", "S!sar get 4", true);

        return message.channel.send({
            embed: embed
        });

    }

    const roles = [roleFinder("Async"), roleFinder("Heroku"), roleFinder("JS"), roleFinder("Rewrite")];

    let choice = args[1]; // can be 1, 2, 3 or 4

    // if the choice is not 1, 2, 3 or 4
    if (/^[1234]$/.test(choice) == false) {
        return message.channel.send("Enter a valid role number!"); // returns error message
    } else {
        choice -= 1; // because array indexing starts from 0. when they choose 1 it should be roles[0]
    }

    switch (type) {

        case "get":
            message.member.addRole(roles[choice]);
            break;

        case "remove":
            message.member.removeRole(roles[choice]);
            break;

        default:
            return; // when it is neither get nor remove
            break;

    }

    message.channel.send("Added the role you wanted!"); // confirmation message

}