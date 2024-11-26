<!-- include start from firewall/blacklisting.xml.i -->
<node name="blacklisting">
  <properties>
    <help>Blacklisting configuration</help>
  </properties>
  <children>
    <node name="settings">
      <properties>
        <help>Common blacklisting settings</help>
      </properties>
      <children>
        <node name="abuseipdb">
          <properties>
            <help>AbuseIPDB settings</help>
          </properties>
          <children>
            <leafNode name="key">
              <properties>
                <help>API key for AbuseIPDB</help>
                <constraint>
                  <regex>([A-Za-z0-9]+)</regex>
                </constraint>
              </properties>
            </leafNode>
          </children>
        </node>
      </children>
    </node>
    <tagNode name="group">
      <properties>
        <help>Blacklisting group</help>
        <constraint>
          <regex>[a-zA-Z0-9][\w\-\.]*</regex>
        </constraint>
      </properties>
      <children>
        <node name="scheduling">
          <properties>
            <help>Common blacklisting settings</help>
          </properties>
          <children>
            <tagNode name="task">
              <properties>
                <help>Scheduled task</help>
                <valueHelp>
                  <format>txt</format>
                  <description>Task name</description>
                </valueHelp>
                <priority>999</priority>
              </properties>
              <children>
                <leafNode name="crontab-spec">
                  <properties>
                    <help>UNIX crontab time specification string</help>
                  </properties>
                </leafNode>
                <leafNode name="interval">
                  <properties>
                    <help>Execution interval</help>
                    <valueHelp>
                      <format>&lt;minutes&gt;</format>
                      <description>Execution interval in minutes</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;minutes&gt;m</format>
                      <description>Execution interval in minutes</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;hours&gt;h</format>
                      <description>Execution interval in hours</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;days&gt;d</format>
                      <description>Execution interval in days</description>
                    </valueHelp>
                    <constraint>
                      <regex>[1-9]([0-9]*)([mhd]{0,1})</regex>
                    </constraint>
                  </properties>
                </leafNode>
              </children>
            </tagNode>
          </children>
        </node>
        <node name="sources">
          <properties>
            <help>Common blacklisting settings</help>
          </properties>
          <children>
            <leafNode name="generic-source">
              <properties>
                <help>A generic source which returns a list of IPs / prefixes.</help>
                <valueHelp>
                  <format>url</format>
                  <description>URL of the data source. Must return a list of IPs / prefixes.</description>
                </valueHelp>
                <priority>999</priority>
                <multi/>
              </properties>
            </leafNode>
            <node name="abuseipdb">
              <properties>
                <help>AbuseIPDB source</help>
              </properties>
              <children>
                <leafNode name="confidence-level">
                  <properties>
                    <help>AbuseIPDB confidence level</help>
                    <valueHelp>
                      <format>0-100</format>
                      <description>AbuseIPDB confidence level 0-100 (default 70)</description>
                    </valueHelp>
                    <constraint>
                      <validator name="numeric" argument="--range 0-100"/>
                    </constraint>
                    <constraintErrorMessage>AbuseIPDB confidence level must be between 0 and 100</constraintErrorMessage>
                  </properties>
                </leafNode>
                <leafNode name="key">
                  <properties>
                    <help>API key for AbuseIPDB. Overrides the default key.</help>
                    <constraint>
                      <regex>([A-Za-z0-9]+)</regex>
                    </constraint>
                  </properties>
                </leafNode>
              </children>
            </node>
          </children>
        </node>
        <node name="filter">
          <properties>
            <help>Filter results</help>
          </properties>
          <children>
            <tagNode name="network">
              <properties>
                <help>Network name</help>
                <constraint>
                  #include <include/constraint/alpha-numeric-hyphen-underscore-dot.xml.i>
                </constraint>
                <constraintErrorMessage>Name of network can only contain alphanumeric letters, hyphen, underscores and dot</constraintErrorMessage>
              </properties>
              <children>
                <leafNode name="network">
                  <properties>
                    <help>Network-group member</help>
                    <valueHelp>
                      <format>ipv4net</format>
                      <description>IPv4 Subnet to match</description>
                    </valueHelp>
                    <constraint>
                      <validator name="ipv4-prefix"/>
                    </constraint>
                    <multi/>
                  </properties>
                </leafNode>
                <leafNode name="firewall-group">
                  <properties>
                    <help>Group name</help>
                    <completionHelp>
                      <path>firewall group network-group</path>
                    </completionHelp>
                    <constraint>
                      #include <include/constraint/alpha-numeric-hyphen-underscore-dot.xml.i>
                    </constraint>
                    <constraintErrorMessage>Name of firewall group can only contain alphanumeric letters, hyphen, underscores and dot</constraintErrorMessage>
                  </properties>
                </leafNode>
              </children>
            </tagNode>
          </children>
        </node>
        <node name="destination">
          <properties>
            <help>Destination</help>
          </properties>
          <children>
            <leafNode name="file">
              <properties>
                <help>file location</help>
              </properties>
            </leafNode>
            <leafNode name="firewall-group">
              <properties>
                <help>Group name</help>
                <constraint>
                  #include <include/constraint/alpha-numeric-hyphen-underscore-dot.xml.i>
                </constraint>
                <constraintErrorMessage>Name of firewall group can only contain alphanumeric letters, hyphen, underscores and dot</constraintErrorMessage>
              </properties>
            </leafNode>
          </children>
        </node>
        <node name="events">
          <properties>
            <help>Events</help>
          </properties>
          <children>
            <node name="before-update">
              <properties>
                <help>Before update</help>
              </properties>
              <children>
                <tagNode name="script">
                  <properties>
                    <help>Script location</help>
                  </properties>
                  <children>
                    <leafNode name="arguments">
                      <properties>
                        <help>Script arguments</help>
                        <multi/>
                      </properties>
                    </leafNode>
                  </children>
                </tagNode>
              </children>
            </node>
            <node name="after-update">
              <properties>
                <help>Before update</help>
              </properties>
              <children>
                <tagNode name="script">
                  <properties>
                    <help>Script location</help>
                  </properties>
                  <children>
                    <leafNode name="arguments">
                      <properties>
                        <help>Script arguments</help>
                      </properties>
                    </leafNode>
                  </children>
                </tagNode>
              </children>
            </node>
          </children>
        </node>
      </children>
    </tagNode>
  </children>
</node>
<!-- include end -->