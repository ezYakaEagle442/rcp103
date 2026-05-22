const fs = require('fs');
const path = require('path');

/**
 * mermaid_class.js
 *
 * usage :
 * node ./mermaid/mermaid_class.js
 * mmdc --version
 * mmdc -i ./mermaid/mermaid_class.mmd -o ./mermaid/mermaid_class.png
 * mmdc -i ./mermaid/mermaid_class.mmd -o ./mermaid/mermaid_class.svg
 * start ./mermaid/mermaid_class.svg
 * 
 ***************************************************************


 * Génère un diagramme Mermaid à partir du modèle fourni.
 * Écrit le diagramme dans mermaid_xxx.mmd et l'affiche sur la console.
 *
 * Utilisation:
 *   cd C:\github\rcp103
 *   sudo apt upgrade nodejs
 *   node --version
 *   printenv
 * 
 * https://nodejs.org/fr/download
 * 
 * curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
 * \. "$HOME/.nvm/nvm.sh"
 * nvm install 24
 * node -v 
 * npm -v # 
 * 
 * https://github.com/puppeteer/puppeteer/issues/14798
 * https://github.com/mermaid-js/mermaid-cli/issues/1019
 * 
 * https://pptr.dev/next/troubleshooting#running-puppeteer-on-wsl-windows-subsystem-for-linux
 * ==> pre-req: 
 * wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
 * sudo apt install -f ./google-chrome-stable_current_amd64.deb
 * 
 * https://pptr.dev/troubleshooting
 * https://pptr.dev/guides/configuration
 * https://pptr.dev/troubleshooting#could-not-find-expected-browser-locally
 * PUPPETEER_CACHE_DIR=('/mnt/c/Users/xxx/.cache/puppeteer') npm install puppeteer
 * PUPPETEER_CACHE_DIR=('/mnt/c/Users/xxx/.cache/puppeteer') node  mermaid_graph.js
 * ls -al /mnt/c/Users/xxx/.cache/puppeteer
 * ls -al ~/.cache/puppeteer
 * ls -al /mnt/c/Users/xxx/AppData/Roaming/npm/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core/lib/esm/puppeteer/node
 * https://medium.com/@python-javascript-php-html-css/fixing-could-not-find-chrome-and-cache-path-problems-on-the-server-with-node-js-puppeteer-507990e718cd
 * 
 * 
 * https://github.com/puppeteer/puppeteer/issues/12006
 * node -i
 * path.join(os.homedir(), '.cache', 'puppeteer')
 * 
 * npx puppeteer browsers install chrome-headless-shell
 * npx puppeteer browsers install chrome
 * npx puppeteer --version
 * npm -g rebuild puppeteer  if you've installed @mermaid-js/mermaid-cli with the -g flag, or npm rebuild puppeteer if you've installed it without the -g flag.
 * npm install -g @mermaid-js/mermaid-cli ==> -g issue : https://github.com/mermaid-js/mermaid-cli/issues/671
 * 
 * node mermaid_graph.js
 * npm rebuild puppeteer
 * npm install @mermaid-js/mermaid-cli --force
 * 
 * mmdc --version
 * mmdc -i mermaid_graph.mmd -o mermaid_graph.svg
 * mmdc -i mermaid_graph.mmd -o mermaid_graph.png
 * start mermaid_graph.svg
 * 
 */



// Load cache path from environment variables
/*
const CACHE_PATH = process.env.PUPPETEER_CACHE_PATH || '/mnt/c/Users/xxx/.cache/puppeteer';
process.env.PUPPETEER_CACHE = CACHE_PATH;

module.exports = {
  cacheDirectory: path.join('/mnt/c/Users/xxx', '.cache', 'puppeteer'),
};
*/

const mermaid = `%%{init: {"theme":"default"}}%%

classDiagram
    class Engine {
        +main()
        +generate_trace()
        +print_metrics()
        +run_tests()
        +create_clients()
        +create_gateway(max_queue_size, nb_servers)
    }

    class GatewayImpl {
        +create_servers()
        +create_queue()
        +receive_message()
        +dispatch()
        +_next_server()
    }

    class ClientImpl {
        +send_message()
    }

    class EventImpl {
        +get_event_type()
        +get_message()
        +read_message()
    }

    class MessageImpl {
        +get_destination()
        +get_timestamp()
        +get_source()
        +get_message_id()
    }

    class QueueImpl {
        +enqueue()
        +dequeue()
        +count_messages()
        +read_messages()
    }

    class SchedulerImpl {
        +add_event()
        +get_events()
        +insert_event()
    }

    class ServerImpl {
        +listen()
        +process_message()
    }

    %% Relations
    Engine --> "1" QueueImpl: instantiates
    GatewayImpl --> "1..*" ServerImpl : creates
    GatewayImpl --> "1" QueueImpl : manages
    Engine --> GatewayImpl : instantiates
    Engine --> "1..*" ClientImpl : creates
    EventImpl --> "1" MessageImpl : has
    QueueImpl --> "1..*" MessageImpl : reads
    SchedulerImpl --> EventImpl : insert_event
    ServerImpl --> QueueImpl : accesses

    `;

const outFile = path.join(__dirname, 'mermaid_class.mmd');

try {
    // console.log('CACHE_PATH:', CACHE_PATH);

    fs.writeFileSync(outFile, mermaid, { encoding: 'utf8' });
    console.log('Mermaid diagram generated:', outFile);
    console.log('--- Diagram preview ---');
    console.log(mermaid);
} catch (err) {
    console.error('Erreur lors de l\'écriture du fichier Mermaid:', err);
    process.exit(1);
}